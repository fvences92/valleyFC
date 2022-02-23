from django.db import models
from django.urls import reverse

# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('divisions_detail', kwargs={'pk': self.id})
# Add the Cat class & list and view function below the imports
class Player(models.Model):  # Note that parens are optional if not inheriting from another class
    name = models.CharField(max_length=100)
    jersey = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    age = models.IntegerField()
    divisions = models.ManyToManyField(Division)

    def __str__(self):
      return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs ={'player_id': self.id})



      
