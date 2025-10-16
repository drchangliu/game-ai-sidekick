import subprocess
import time

max_calls = [1, 3, 5, 10]
num_runs = 20

delay_seconds = 5

for max_call in max_calls:
    print(f"\nmax_calls={max_call}")
    try:
        subprocess.run(
            ["python", "llm_tests.py", "--max_calls", str(max_call), "--runs", str(num_runs)],
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"(max_calls={max_call})")
    
    print(f"Waiting {delay_seconds}s before next run...\n")
    time.sleep(delay_seconds)

print("All benchmarks completed!")
