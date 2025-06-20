import itertools
import string
from progressbar import progressbar

def is_valid(candidate):
    # Split by spaces to get "words"
    words = candidate.strip().split()
    for word in words:
        if len(word) == 1 and word.upper() not in ('A', 'I'):
            return False
    return True

def generate_wordlist(output_file):
    chars = string.ascii_lowercase + string.digits

    with open(output_file, "w", encoding="utf8") as f:
        # Try all possible lengths from 5 (minimum with 4 spaces) up to 30
        for length in range(5, 31):
            space_combos = list(itertools.combinations(range(1, length - 1), 4))
            for space_positions in progressbar(space_combos, prefix=f"Length {length}: "):
                # Skip if any spaces are adjacent
                if any(b - a == 1 for a, b in zip(space_positions, space_positions[1:])):
                    continue
                fill_indices = [i for i in range(length) if i not in space_positions]
                for first_char in string.ascii_uppercase:
                    for fill in itertools.product(chars, repeat=len(fill_indices) - 1):
                        word = [""] * length
                        word[0] = first_char
                        fill_ptr = 0
                        for i in range(1, length):
                            if i in space_positions:
                                word[i] = " "
                            else:
                                word[i] = fill[fill_ptr]
                                fill_ptr += 1
                        candidate = "".join(word)
                        if is_valid(candidate):
                            f.write(candidate + "\n")
