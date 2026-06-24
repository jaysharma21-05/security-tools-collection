import re
import math

def check_length(password):
    length = len(password)
    if length < 6:
        return 0, "Too short (minimum 6 characters)"
    elif length < 8:
        return 1, "Short (8+ recommended)"
    elif length < 12:
        return 2, "Good length"
    else:
        return 3, "Excellent length"

def check_uppercase(password):
    if re.search(r'[A-Z]', password):
        return 1, "Has uppercase ✓"
    return 0, "No uppercase letter"

def check_lowercase(password):
    if re.search(r'[a-z]', password):
        return 1, "Has lowercase ✓"
    return 0, "No lowercase letter"

def check_numbers(password):
    if re.search(r'[0-9]', password):
        return 1, "Has numbers ✓"
    return 0, "No numbers found"

def check_special(password):
    if re.search(r'[!@#$%^&*(),.?\":{}|<>]', password):
        return 2, "Has special characters ✓"
    return 0, "No special characters"

def calculate_entropy(password):
    charset = 0
    if re.search(r'[a-z]', password): charset += 26
    if re.search(r'[A-Z]', password): charset += 26
    if re.search(r'[0-9]', password): charset += 10
    if re.search(r'[^a-zA-Z0-9]', password): charset += 32

    if charset == 0:
        return 0

    entropy = len(password) * math.log2(charset)
    return round(entropy, 2)

def get_strength_label(score, entropy):
    if score <= 2 or entropy < 28:
        return "WEAK 🔴"
    elif score <= 4 or entropy < 40:
        return "MODERATE 🟡"
    elif score <= 6 or entropy < 55:
        return "STRONG 🟢"
    else:
        return "VERY STRONG 💪"

def analyze_password(password):
    print("\n" + "="*45)
    print(f"  Analyzing: {'*' * len(password)}")
    print("="*45)

    total_score = 0
    suggestions = []

    checks = [
        check_length(password),
        check_uppercase(password),
        check_lowercase(password),
        check_numbers(password),
        check_special(password),
    ]

    for score, message in checks:
        total_score += score
        status = "✓" if score > 0 else "✗"
        print(f"  [{status}] {message}")
        if score == 0:
            suggestions.append(f"Add {message.replace('No ', '').replace(' found', '')}")

    entropy = calculate_entropy(password)
    strength = get_strength_label(total_score, entropy)

    print(f"\n  Entropy Score : {entropy} bits")
    print(f"  Total Score   : {total_score}/8")
    print(f"  Strength      : {strength}")

    if suggestions:
        print("\n  Suggestions to improve:")
        for tip in suggestions:
            print(f"    → {tip}")

    print("="*45 + "\n")

def main():
    print("\n🔐 Password Strength Analyzer")
    print("   Educational Tool | Python + Cybersecurity")
    print("-" * 45)

    while True:
        password = input("\nEnter password to analyze (or 'quit' to exit): ")

        if password.lower() == 'quit':
            print("\n[*] Exiting. Stay secure! 👋\n")
            break

        if not password:
            print("[!] Please enter a password.")
            continue

        analyze_password(password)

if __name__ == "__main__":
    main()
