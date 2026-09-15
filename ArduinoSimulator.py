from tqdm import tqdm
import time

def move_stepper(steps, direction, speed_micros=1000):
    dir_str = "FORWARD" if direction else "REVERSE"
    print(f"Step Motor → {dir_str} for {steps} steps.")
    print(f"(Delay between steps: {speed_micros}μs)")

    # Convert microseconds to seconds
    delay_seconds = speed_micros / 1_000_000

    for _ in tqdm(range(steps), desc="Stepping", unit="step"):
        time.sleep(delay_seconds)

def simulate_actuator_sequence(step_a, step_b):
    print("Actuator Triggered!")
    print(f"Step A = {step_a}, Step B = {step_b}")

    print(f"Moving out {step_a} steps...")
    move_stepper(step_a, direction=True)
    print("Pausing after A... [3 seconds simulated]")

    print(f"Moving out {step_b} steps...")
    move_stepper(step_b, direction=True)
    print("Pausing after B... [5 seconds simulated]")

    print(f"Retracting {step_a + step_b} steps...")
    move_stepper(step_a + step_b, direction=False)

    print("Actuator Deployment Complete.\n")

# === Simulate input ===
user_input_a = 500
user_input_b = 800
simulate_actuator_sequence(user_input_a, user_input_b)