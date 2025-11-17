# Wordle/Fibble LLM Solver Competition

Use any LLMs to help solve the Wordle (6 tries) or the Fibble (9 tries, with 1, 2, 3, 4, or 5 lies per guess) problems. Collect win rates and other metrics for 10 games for each commericial LLMs with API Key-based access and 1000 games for locally deployed LLMs. It is acceptable if you only have Wordle results or Fibble-with-one-lie results.

Here are two examples of how ChatGPT helps solve the original Fibble probelm.
### Example 1
<img width="134" height="274" alt="Screenshot 2025-11-04 at 5 58 44 PM" src="https://github.com/user-attachments/assets/523c979b-30ba-4cbd-8690-72749b6f91cb" />

* https://chatgpt.com/share/690a84e3-5df8-8001-ac9e-799ac4350f25

### Example 2
* https://chatgpt.com/share/690a60fd-302c-800b-94dc-64addd79beb7
  
Note that your submission must use LLMs to solve Wordle/Fibble via programs, not through human-in-the-loop manual chats with an LLM chatbot.

### Metrics:
* Win rate
* Average no. of guesses per winning game
* Latency per LLM call
* Average number of LLM calls per guess
* Ratio of invalid guesses versus valid guesses (or percentage of LLM guesses that are invalid or self-contradicting)
* Average size of prompts

When the win rates are the same, the one with fewer guesses wins.

You can use the [headstart code provided in this repo](https://github.com/drchangliu/game-ai-sidekick/blob/main/wordle/src/llm_tests.py), or the OCaml headstart code provided in CS3200.

The use of LLMs in planning, coding, debugging, testing, and prompt generating/adjustment is encourage. Just make sure all usage is documented in the README.md file.

### Submission: 
https://docs.google.com/forms/d/e/1FAIpQLSd3_25EQeDTSQkmms8wj5FSQQ4SkOoo7Cyzr9EDUZRcSf2rrg/viewform?usp=header 

### Deadline: 
* Round 1: December 9, 2025. End of the Day. Anywhere on Earth.

### Current Best Result:

Note that in the original Fibble, lies can be any column. In our current version of Python implementation, lies will always be in the same column, even though that's still randomly selected.

OpenAI GPT-5 with low reasoning achieved the following win rates for the same-column-lies version:
* fibble1 - Win Rate: 100% in 10 games, Avg Tries: 5.9
* fibble2 - Win Rate: 100% in 10 games, Avg Tries: 6.5
* fibble3 - Win Rate: 70% in 10 games, Avg Tries: 7.5
* fibble4 - Win Rate: 0% in 10 games, Avg Tries: 9.0
* fibble5 - Win Rate: 90% in 10 games, Avg Tries: 6.9











