import "dotenv/config";
import * as fs from 'node:fs';
import { exit } from "node:process";
import OpenAI from "openai";
import { zodResponseFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI({
    apiKey: process.env.API_KEY
});

const numLines = 1001;
const fileData = fs.readFileSync('./games.txt', 'utf8');
const lines = fileData.split(/\r?\n/); // Split on '\r\n' or '\n'
const gamesData = lines.slice(0, numLines-1).join('\n');

// Prompting Settings
const model = "4o";
const tests = 100;
const delay = 5000; // delay for rate limit (ms)
const outputFile = `./${model}-rules.json`;

// Replace this with whichever pre-prompt combination you are interested in
const prePrompt = `
Game Rules:
Two players, Player 1 and Player 2, take turns making one move per turn. Each player has two counters that cannot count exceed 4; if a counter is greater than or equal to 5 then that counter is reset to 0.
On a turn a player can choose one of two actions:
- Attack: Select one of your counters and add its value to an opponent’s counter. You cannot attack with a 0 counter or target a 0 counter. Example: If your counter is 2 and you attack an opponent’s counter with 1, their counter becomes 3, and your counter remains 2.
- Split: Revive a 0 counter by moving half the value of your non-zero, even counter to the 0 counter. You can only split if one counter is 0 and the other is even. Example: If your counters are 0 and 4, after splitting, they become 2 and 2.
The game is over when both of a player's counters are 0, and thus cannot continue to play. The player that does not have both counters at 0 wins the game.

Game State Format:
Game states are represented as [ABCD], where AB are the counters of the player about to move. After a move, AB and CD swap to reflect the opposing player’s counters.

Move Format:
- Attack: "A:Y Z", where A=Attack, Y=your counter letter (A or B), Z=opponent's counter letter (C or D).
- Split: "S:Y", where S=Split, Y=your non-zero, even counter letter (A or B).
`;

// Change the constant game state here
const gameState = `
You are Player 1.
It’s your turn.
The current game state is [3321].
What is the best move?`;

// Include this at the end of the prompt for o1 support
const jsonFormatPrompt = `
Respond only in valid JSON format as specified:
{
    \"thinking\": \"Chain of Thought thinking here\",
    \"primary_move\": \"A:A D\",
    \"primary_move_reason\": \"I chose this move because...\"
}
`;

const textPrompt = `${prePrompt}${gameState}`;

const GameMove = z.object({
    thinking: z.string(),
    primary_move: z.string(),
    primary_move_reason: z.string()
});

async function prompt(content) {
    try {
        const completion = await openai.chat.completions.create({
            model: model,
            store: true,
            messages: [
                { "role": "user", "content": content }
            ],
            response_format: zodResponseFormat(GameMove, "move")
        });

        return completion.choices[0].message.content;
    } catch (error) {
        return `{\"PROMPT ERROR\":\"${error}\"}`
    }

}

function appendJSONToFile(filePath, json) {
    let data = [];

    // Check if the file exists
    if (fs.existsSync(filePath)) {
        // Read the existing file content
        const fileContent = fs.readFileSync(filePath, 'utf8');
        try {
            // Parse it as JSON if valid
            data = JSON.parse(fileContent);
        } catch (err) {
            console.error('Invalid JSON format in the file.');
            return;
        }
    }

    // Append the new object to the data
    data.push(json);

    // Write the updated data back to the file
    fs.writeFileSync(filePath, JSON.stringify(data, null, 2));
}

const sleep = (ms) => new Promise(resolve => setTimeout(resolve, ms));

async function main() {
    for (let i = 0; i < tests; i++) {
        console.log(`Running prompt ${i}/${tests}...`)
        const response = await prompt(textPrompt);
        const outputJSON = JSON.parse(response);
        appendJSONToFile(outputFile, outputJSON);
        await sleep(delay);
    }
    console.log(`Finished, check ${outputFile}`);
}

main();