from django.urls import path
from .views import NewGameView, GameStateView, GuessView

urlpatterns = [
    path("new", NewGameView.as_view(), name="new game"),
    path("<int:id>", GameStateView.as_view(), name="game state"),
    path("<int:id>/guess", GuessView.as_view(), name="guess"),
]