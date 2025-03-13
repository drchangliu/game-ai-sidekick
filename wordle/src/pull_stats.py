from firebase import get_db, initialize_firebase

if __name__ == '__main__':
    initialize_firebase()
    db = get_db()

    games = list(map(lambda x: x.to_dict(), db.collection('games').get()))

    total_llm_guesses = 0
    total_llm_retries = 0
    accepted_llm_guesses = 0

    for game in games:
        for llm_guess in game['llm_guesses']:
            total_llm_guesses += 1
            total_llm_retries += llm_guess['retries']
            if llm_guess['accepted']:
                accepted_llm_guesses += 1

    avg_llm_retries = total_llm_retries / total_llm_guesses
    avg_accepted_llm_guesses = accepted_llm_guesses / total_llm_guesses

    print(f'Total LLM Guesses: {total_llm_guesses}')
    print(f'Total LLM Retries: {total_llm_retries}')
    print(f'Total Accepted LLM Guesses: {accepted_llm_guesses}')
    print()
    print(f'Average LLM Retries: {avg_llm_retries}')
    print(f'LLM guess acceptance rate: {avg_accepted_llm_guesses * 100}%')
