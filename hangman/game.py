from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, guess_letter, hit=None, miss=None):
        if hit is True and miss is True:
            raise InvalidGuessAttempt('Guess letter cannot be a hit and a miss')
        guess_letter_lower = guess_letter.lower()
        self.guess_letter = guess_letter_lower
        self.hit = hit
        self.miss = miss
    
    def is_hit(self):
        if self.hit is True:
            return True
        return False
    
    def is_miss(self):
        if self.miss is True:
            return True
        return False


class GuessWord(object):
    def __init__(self, guess_word):
        if not guess_word:
            raise InvalidWordException('Guess word cannot be empty')
        guess_word_lower = guess_word.lower()
        self.answer = guess_word_lower
        self.masked = '*' * len(guess_word_lower)
    
    def perform_attempt(self, guess_letter):
        if len(guess_letter) > 1:
            raise InvalidGuessedLetterException('Only guess 1 character')
        guess_letter_lower = guess_letter.lower()
        masked = self.masked.lower()
        answer = self.answer.lower()
        if guess_letter_lower in answer:
            updated_masked = ''
            for index, char in enumerate(answer):
                if char == guess_letter_lower or char == masked[index]:
                    updated_masked += char
                else:
                    updated_masked += '*'
            self.masked = updated_masked
            attempt = GuessAttempt(guess_letter_lower, hit=True)
        else:
            attempt = GuessAttempt(guess_letter_lower, miss=True)
        return attempt

class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    
    def __init__(self, word_list=None, number_of_guesses=5):
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        if word_list:
            random_word = self.select_random_word(word_list)
        else:
            random_word = self.select_random_word(self.WORD_LIST)
        self.word = GuessWord(random_word)
    
    def guess(self, guess_letter):
        if self.is_finished():
            raise GameFinishedException('Out of guesses')
            
        guess_letter_lower = guess_letter.lower()
        attempt = self.word.perform_attempt(guess_letter_lower)
        if attempt.is_miss():
            self.remaining_misses -= 1
        if guess_letter_lower not in self.previous_guesses:
            self.previous_guesses.append(guess_letter_lower)
            
        if self.is_won():
            raise GameWonException('You win!')
        if self.is_lost():
            raise GameLostException('Better luck next time!')
            
        return attempt
    
    def is_finished(self):
        if self.is_won() or self.is_lost() or self.remaining_misses <= 0:
            return True
        return False
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
    
    def is_lost(self):
        if self.word.answer != self.word.masked and self.remaining_misses <= 0:
            return True
        return False
        
    @classmethod 
    def select_random_word(cls, list_of_words):
        if not list_of_words:
            raise InvalidListOfWordsException()
        return random.choice(list_of_words)