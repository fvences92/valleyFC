from pyexpat import model
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import login
from .models import Player, Division
from .forms import RecordForm
import boto3
import uuid


S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'valleyfc'


def signup(request):
    # handle POST Requests (signing up)
    error_message = ''
    if request.method == 'POST':
        # <= fills out the form with the form values from the request
        form = UserCreationForm(request.POST)
        # validate form inputs
        if form.is_valid():
            # save the new user to the database
            user = form.save()
            # log the user in
            login(request, user)
            # redirect the user to the dogs index
            return redirect('index')
        else:
            # if the user form is invalid - show an error message
            error_message = 'invalid credentials - please try again'
    # handle GET Requests (navigating the user to the signup page)
    # present the user with a fresh signup form
    form = UserCreationForm()
    context = {'form': form, 'error': error_message}
    return render(request, 'registration/signup.html', context)



@login_required
def home(request):
  return render(request, 'home.html')

@login_required
def about(request):
  return render(request, 'about.html')

@login_required
def players_index(request):
    players = Player.objects.all()
    return render(request, 'players/index.html', { 'players': players})

@login_required
def players_detail(request, player_id):
  player = Player.objects.get(id=player_id)
  # instantiate RecordForm to be rendered in the template
  record_form = RecordForm()

  # displaying unassociated divisions
  divisions_player_doesnt_have = Division.objects.exclude(id__in = player.divisions.all().values_list('id'))

  return render(request, 'players/detail.html', {
    # include the player and record_form in the context
    'player': player,
    'record_form': record_form,
    'divisions' : divisions_player_doesnt_have,
  })

@login_required
def add_record(request, player_id):
    form = RecordForm(request.POST)
    if form.is_valid():
        new_record = form.save(commit=False)
        new_record.player_id = player_id
        new_record.save()
    return redirect('detail', player_id=player_id)

@login_required
def assoc_division(request, player_id, division_id):
  # Note that you can pass a toy's id instead of the whole object
   Player.objects.get(id=player_id).divisions.add(division_id)
   return redirect('detail', player_id=player_id)

class PlayerCreate(LoginRequiredMixin, CreateView):
  model = Player
  fields = '__all__'
  
  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
    #seuccess_url = '/players/'

class PlayerUpdate(LoginRequiredMixin, UpdateView):
  model = Player
  # Let's disallow the renaming of a player by excluding the name field!
  fields = ['jersey', 'position', 'age']

class PlayerDelete(LoginRequiredMixin, DeleteView):
  model = Player
  success_url = '/players/'

class DivisionCreate(LoginRequiredMixin, CreateView):
    model = Division
    fields = ('name', 'color')


class DivisionUpdate(LoginRequiredMixin, UpdateView):
    model = Division
    fields = ('name', 'color')


class DivisionDelete(LoginRequiredMixin, DeleteView):
    model = Division
    success_url = '/divisions/'


class DivisionDetail(LoginRequiredMixin, DetailView):
    model = Division
    template_name = 'divisions/detail.html'


class DivisionList(LoginRequiredMixin, ListView):
    model = Division
    template_name = 'divisions/index.html'