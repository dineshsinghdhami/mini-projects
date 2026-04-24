import random

word_list = ['python','java','html','css','javascript','php']

def display_word(word, guessed):
    display = ''
    for letter in word:
        if letter in guessed:
            display += letter
        else:
            display += '_'
    return display

def hangman():
    word = random.choice(word_list)
    guessed_letter = set()
    attempts = 6

    print("Welcome to Hangman Game")

    while attempts > 0:
        print(f"word : {display_word(word, guessed_letter)}")
        print(f"guessed letters : {' '.join(guessed_letter)}")
        print(f"remaining attempts : {attempts}")

        guess = input("Guess the letter: ").lower()

        if guess in guessed_letter:
            print("Already guessed!")
            continue

        guessed_letter.add(guess)

        if guess in word:
            print("Good Guess")
        else:
            print("Wrong Guess")
            attempts -= 1

        if "_" not in display_word(word, guessed_letter):
            print("Congratulations, you won!")
            print(f"The word was: {word}")
            break
    else:
        print("You failed!")
        print(f"The word was: {word}")

if __name__ == "__main__":
    hangman()
