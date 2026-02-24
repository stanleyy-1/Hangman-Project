import random
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Game
from .serializers import GameStateSerializer


# Create your views here.

WORD_LIST = ["Hangman", "Python", "Audacix", "Bottle", "Pen"]
class NewGameView(APIView):
    def post(self, request):
        word = random.choice(WORD_LIST)
        game = Game.objects.create(word=word)
        return Response({"id": game.id}, status=status.HTTP_201_CREATED)


class GameStateView(APIView):
    def get(self, request, id):
        try:
            game = Game.objects.get(pk=id)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = GameStateSerializer(game)
        return Response(serializer.data)


class GuessView(APIView):
    def post(self, request, id):
        try:
            game = Game.objects.get(pk=id)
        except Game.DoesNotExist:
            return Response({"error": "Game not found."}, status=status.HTTP_404_NOT_FOUND)

        letter = request.data.get("letter", "")

        if not isinstance(letter, str) or len(letter) != 1 or not letter.isalpha():
            return Response(
                {"error": "Provide exactly one alphabetic character as 'letter'."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if game.game_state != Game.STATE_IN_PROGRESS:
            serializer = GameStateSerializer(game)
            data = serializer.data
            data["correct"] = None
            data["message"] = "Game is already over."
            return Response(data)
        
        if letter.lower() in game.guessed_letters:
            serializer = GameStateSerializer(game)
            data = serializer.data
            data["correct"] = None
            data["message"] = "Letter already guessed."
            return Response(data)

        correct = game.make_guess(letter)
        serializer = GameStateSerializer(game)
        data = serializer.data
        data["correct"] = correct
        return Response(data)
    
def index(request):
    return render(request, "index.html")