from pyexpat import model
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Player, Division
from .forms import RecordForm



S3_BASE_URL = 'https://s3.us-east-1.amazonaws.com/'
BUCKET = 'valleyfc'


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A bad POST or a GET request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


def home(request):
  return render(request, 'home.html')

def about(request):
  return render(request, 'about.html')

@login_required
def players_index(request):
    players = Player.objects.filter(user=request.user)
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
  fields = ('name','jersey', 'position', 'age')
  success_url = '/players/'

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)

class PlayerUpdate(LoginRequiredMixin, UpdateView):
  model = Player
  # Let's disallow the renaming of a player by excluding the name field!
  fields = ('name', 'jersey', 'position', 'age')

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


class DivisionDetail(DetailView):
    model = Division
    template_name = 'divisions/detail.html'


class DivisionList(ListView):
    model = Division
    template_name = 'divisions/index.html'