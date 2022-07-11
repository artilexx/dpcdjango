from django.shortcuts import render
from website.functions.get_player_stats import get_player_stats

# Create your views here.
def homepage(request):
    return get_player_stats(request, player = "Arteezy") #set default player/homepage to arteezy

def playerpage(request, player):
    return get_player_stats(request, player)
