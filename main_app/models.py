from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

STATS = (
    ('G', 'Goal'),
    ('A', 'Assist'),
    ('B', 'Block'),
)
# Create your models here.


class Division(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)

    def get_absolute_url(self):
        return reverse('divisions_detail', kwargs={'pk': self.id})
# Add the player class & list and view function below the imports


class Player(models.Model):  # Note that parens are optional if not inheriting from another class
    name = models.CharField(max_length=100)
    jersey = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    age = models.IntegerField()
    divisions = models.ManyToManyField(Division)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=2)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail', kwargs={'player_id': self.id})


class Record(models.Model):
    date = models.DateField('Stat Date')
    stat = models.CharField(
        max_length=1,
        choices=STATS,
        default=STATS[0][0]
    )

    player = models.ForeignKey(Player, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.get_stat_display()} on {self.date}"

    # change the default sort
    class Meta:
        ordering = ['-date']
