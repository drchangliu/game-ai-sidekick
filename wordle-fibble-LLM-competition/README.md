# Wordle/Fibble LLM Solver Competition

Use any LLMs to help solve the Wordle (6 tries) or the Fibble (9 tries, with 1, 2, 3, 4, or 5 lies per guess) problems. Collect win rates and other metrics for 10 games for each commericial LLMs with API Key-based access and 1000 games for locally deployed LLMs. It is acceptable if you only have Wordle results or Fibble-with-one-lie results.

Here are two examples of how ChatGPT helps solve the Fibble probelm.
* https://chatgpt.com/share/690a84e3-5df8-8001-ac9e-799ac4350f25
* https://chatgpt.com/share/690a60fd-302c-800b-94dc-64addd79beb7
  
Note that your submission must use LLMs to solve Wordle/Fibble via programs, not through human-in-the-loop manual chats with an LLM chatbot.

Metrics:
* Win rate
* Average no. of guesses per winning game
* Latency per LLM call
* Average number of LLM calls per guess
* Ratio of invalid guesses versus valid guesses (or percentage of LLM guesses that are invalid or self-contradicting)
* Average size of prompts

When the win rates are the same, the one with fewer guesses wins.

You can use the [headstart code provided in this repo](https://github.com/drchangliu/game-ai-sidekick/blob/main/wordle/src/llm_tests.py), or the OCaml headstart code provided in CS3200.

The use of LLMs in planning, coding, debugging, testing, and prompt generating/adjustment is encourage. Just make sure all usage is documented in the README.md file.

Submission: https://docs.google.com/forms/d/e/1FAIpQLSd3_25EQeDTSQkmms8wj5FSQQ4SkOoo7Cyzr9EDUZRcSf2rrg/viewform?usp=header 





