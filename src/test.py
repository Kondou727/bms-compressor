import time

for i in range(10):
    print(f"Processing file {i}", end='\r', flush=True)
    time.sleep(0.5)
print()  # Final newline at the end