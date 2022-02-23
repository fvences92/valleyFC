from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('players/', views.players_index, name='index'),
    path('players/<int:player_id>/', views.players_detail, name='detail'),
    path('players/create/', views.PlayerCreate.as_view(), name='players_create'),
    path('players/<int:pk>/update/', views.PlayerUpdate.as_view(), name='players_update'),
    path('players/<int:pk>/delete/', views.PlayerDelete.as_view(), name='players_delete'),
    path('divisions/', views.DivisionsList.as_view(), name='divisions_index'),
    path('divisions/<int:pk>/', views.DivisionDetail.as_view(), name='Divisions_detail'),
    path('divisions/create/', views.DivisionCreate.as_view(), name='divisions_create'),
    path('divisions/<int:pk>/update/', views.DivisionUpdate.as_view(), name='division_update'),
    path('divisions/<int:pk>/delete/', views.DivisionDelete.as_view(), name='division_delete'),
    path('players/<int:player_id>/assoc_division/<int:division_id>/', views.assoc_division, name='assoc_division'),
]
