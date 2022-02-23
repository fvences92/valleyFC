from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.views.generic import ListView
from .models import Player, Division
from django.contrib.auth.forms import UserCreationForm
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import RecordForm
import boto3
import uuid



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

# update this view function
def players_detail(request, player_id):
  player = Player.objects.get(id=player_id)
  # instantiate RecordForm to be rendered in the template
  record_form = RecordForm()

  # displaying unassociated divisions
  divisions_player_doesnt_have = Division.objects.exclude(id__in = player.divisions.all().values_list('id'))

  return render(request, 'cats/detail.html', {
    # include the player and record_form in the context
    'player': player,
    'record_form': record_form,
    'divisions' : divisions_player_doesnt_have,
  })

def add_record(request, player_id):
    form = RecordForm(request.POST)
    if form.is_valid():
        new_record = form.save(commit=False)
        new_record.player_id = player_id
        new_record.save()
    return redirect('detail', player_id=player_id)

def assoc_division(request, player_id, division_id):
  # Note that you can pass a toy's id instead of the whole object
   Player.objects.get(id=player_id).divisions.add(division_id)
   return redirect('detail', player_id=player_id)

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