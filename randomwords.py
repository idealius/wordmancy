import random
import keyboard
import argparse
import nltk
from nltk.corpus import words, names
import urllib.request
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Argument parsing
parser = argparse.ArgumentParser(description="Generate random English words on spacebar press.")
parser.add_argument('--count', type=int, help="Number of words to generate automatically (skips prompt)")
args = parser.parse_args()

# Download required nltk corpora
nltk.download('words', quiet=True)
nltk.download('names', quiet=True)

# Load word sets
all_words = set(w.lower() for w in words.words())
name_set = set(name.lower() for name in names.words())

# Download common word list
common_url = 'https://raw.githubusercontent.com/first20hours/google-10000-english/master/20k.txt'
response = urllib.request.urlopen(common_url)
common_words = set(w.decode('utf-8').strip().lower() for w in response.readlines())

# Filter out names and non-alphabetic words
common_pool = [w for w in all_words & common_words if w.isalpha() and w not in name_set]
rare_pool = [w for w in all_words - common_words if w.isalpha() and w not in name_set]

# Default or prompt for word count
if args.count is not None:
    word_count = args.count
else:
    try:
        user_input = input("How many random words would you like to generate? (Press Enter for 5): ")
        word_count = int(user_input) if user_input.strip() else 5
    except ValueError:
        print("Invalid input, defaulting to 5 words.")
        word_count = 5

# Word coloring options (exclude black)
color_list = [
    Fore.RED, Fore.GREEN, Fore.YELLOW, Fore.BLUE,
    Fore.MAGENTA, Fore.CYAN, Fore.LIGHTRED_EX,
    Fore.LIGHTGREEN_EX, Fore.LIGHTYELLOW_EX,
    Fore.LIGHTBLUE_EX, Fore.LIGHTMAGENTA_EX, Fore.LIGHTCYAN_EX
]

def get_weighted_random_words(count):
    results = []
    for _ in range(count):
        pool = rare_pool if random.randint(1, 8) == 1 else common_pool
        results.append(random.choice(pool))
    return results

def print_colored_words(words):
    for i in range(0, len(words), 5):
        group = words[i:i+5]
        for word in group:
            color = random.choice(color_list)
            print(color + word, end='  ')
        print("\n")

print(f"\nPress SPACEBAR to generate {word_count} random word(s). Press ESC to exit.")

# If script is run with arguments, generate words once and exit
if args.count is not None:
    word_batch = get_weighted_random_words(args.count)
    print_colored_words(word_batch)
    exit()

# Otherwise, enter interactive mode
print(f"\nPress SPACEBAR to generate {word_count} random word(s). Press ESC to exit.")

while True:
    if keyboard.is_pressed('space'):
        print()
        word_batch = get_weighted_random_words(word_count)
        print_colored_words(word_batch)
        keyboard.wait('space')

    if keyboard.is_pressed('esc'):
        print("Exiting...")
        break

