import math
from django.db import models

# Create your models here.
class Game(models.Model):
    STATE_IN_PROGRESS = "InProgress"
    STATE_WON = "Won"
    STATE_LOST = "Lost"

    STATE_CHOICES = [
        (STATE_IN_PROGRESS, "InProgress"),
        (STATE_WON, "Won"),
        (STATE_LOST, "Lost"),
    ]

    word  = models.CharField(max_length=100)
    game_state = models.CharField(max_length=10, choices=STATE_CHOICES, default=STATE_IN_PROGRESS)
    guessed_letters = models.JSONField(default=list)    # all lowercase
    incorrect_guesses = models.IntegerField(default=0)
    max_incorrect_guesses = models.IntegerField()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.max_incorrect_guesses = math.ceil(len(self.word) / 2)
        super().save(*args, **kwargs)

    @property
    def word_state(self):
        return "".join(c if c.lower() in self.guessed_letters else "_" for c in self.word)
    
    @property
    def incorrect_guesses_remaining(self):
        return max(0, self.max_incorrect_guesses - self.incorrect_guesses)

    def make_guess(self, letter):
        letter = letter.lower()

        if self.game_state != self.STATE_IN_PROGRESS:
            return None

        if letter in [c.lower() for c in self.guessed_letters]:
            return None

        self.guessed_letters.append(letter)

        if letter in self.word.lower():
            correct = True
        else:
            self.incorrect_guesses += 1
            correct = False

        self._update_game_state()
        return correct
    
    def _update_game_state(self):
        if all(c.lower() in self.guessed_letters for c in self.word):
            self.game_state = self.STATE_WON
        elif self.incorrect_guesses >= self.max_incorrect_guesses:
            self.game_state = self.STATE_LOST
        self.save()

    def __str__(self):
        return f"Game {self.pk}: {self.word} [{self.game_state}]"
