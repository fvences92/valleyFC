from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .models import Player, Division
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView


# environment variables
S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'valleyfc'


# Define the home view
def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')


# Add new view
def players_index(request):
    players = Player.objects.all()
    return render(request, 'players/index.html', { 'players': players})

def players_detail(request, player_id):
  player = Player.objects.get(id=player_id)
  return render(request, 'players/detail.html', { 'player': player })

def assoc_division(request, player_id, division_id):
    # Note that you can pass a toy's id instead of the whole object
    Division.objects.get(id=division_id).divisions.add(division_id)
    return redirect('detail', division_id=division_id)

class PlayerCreate(CreateView):
  model = Player
  fields = '__all__'
  success_url = '/players/'

class PlayerUpdate(UpdateView):
  model = Player
  # Let's disallow the renaming of a cat by excluding the name field!
  fields = ['jersey', 'position', 'age']

class PlayerDelete(DeleteView):
  model = Player
  success_url = '/players/'

class DivisionCreate(CreateView):
    model = Division
    fields = ('name', 'color')


class DivisionUpdate(UpdateView):
    model = Division
    fields = ('name', 'color')


class DivisionDelete(DeleteView):
    model = Division
    success_url = '/divisions/'


class DivisionDetail(DetailView):
    model = Division
    template_name = 'divisions/detail.html'


class DivisionList(ListView):
    model = Division
    template_name = 'divisions/index.html'