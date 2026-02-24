from rest_framework import serializers
from .models import Game


class GameStateSerializer(serializers.ModelSerializer):
    word_state = serializers.ReadOnlyField()
    incorrect_guesses_remaining = serializers.ReadOnlyField()

    class Meta:
        model = Game
        fields = [
            "id",
            "game_state",
            "word_state",
            "incorrect_guesses",
            "incorrect_guesses_remaining",
            "guessed_letters",
            "word",
        ]