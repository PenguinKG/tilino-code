import random

def generate_random_3_digit():
    """Generate a random 3-digit number (100-999)."""
    return random.randint(100, 999)

if __name__ == "__main__":
    print(f"Random 3-digit number: {generate_random_3_digit()}")
