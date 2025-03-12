import "dotenv/config";
import * as fs from 'node:fs';
import OpenAI from "openai";
import { zodResponseFormat } from "openai/helpers/zod";
import { z } from "zod";

const openai = new OpenAI({
    apiKey: process.env.API_KEY
});

const numLines = 1033; // 46 games
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
Two players, Player 1 and Player 2, take turns making one move per turn. The game is played on a 6 tall, 7 wide grid, where players place pieces in columns. Players alternate turns, and the goal is to be the first to create a sequence of four of their pieces in a row, column, or diagonal.
On a turn, a player must:
- Place a piece: Select a column (1-7) to place their piece. The piece will fall to the lowest available space in that column.
The game ends when a player creates a sequence of four of their pieces in a row, column, or diagonal. That player wins. If the grid is completely filled, and no player has created a sequence of four. In this case, the game is a draw.

Game State Format:
Game states are represented as a grid of 0, 1, and 2's. For example, [0000000;0000000;0001000;0002000;0012000;0121000;], where '0' represents an empty space, '1' represents Player 1's pieces, and '2' represents Player 2's pieces.

Move Format:
Moves are represented as a single number, corresponding to the column (1-7) where the player places their piece.
`;

// Change the constant game state here
const gameState = `You are Player 1.
It's your turn.
The current game state is [0202200;0101100;0101100;0201100;0122202;2211202].
What is the best move?`;

// Include this at the end of the prompt for o1 support
const jsonFormatPrompt = `
Respond only in valid JSON format as specified:
{
    \"thinking\": \"Chain of Thought thinking here\",
    \"primary_move\": \"Put your final move here.\",
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
        const outputJSON = { o1_response: response };
        appendJSONToFile(outputFile, outputJSON);
        await sleep(delay);
    }
    console.log(`Finished, check ${outputFile}`);
}

main();