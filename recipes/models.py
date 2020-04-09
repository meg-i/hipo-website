from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator


class Ingredient(models.Model):
    
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name 

    
class Recipe(models.Model):

    DIFFICULTY_CHOICES = [
        ("e", "Easy"),
        ("m", "Medium"),
        ("a", "Advanced")
    ]

    ingredients = models.ManyToManyField(Ingredient, related_name="recipes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recipes")
    name = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.TextField()
    date_created = models.DateTimeField(default=timezone.now, editable=False)
    difficulty = models.CharField(max_length=1, choices=DIFFICULTY_CHOICES)
    
    def __str__(self):
        return "{name} by {username}".format(name=self.name, username=self.user.username) 
    
    @property
    def like_count(self):
        return self.likes.count()


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="likes")

    class Meta:
        unique_together = ("user", "recipe")


class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ratings")
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name="ratings")
    rate = models.IntegerField(default=0, validators=[MaxValueValidator(5),MinValueValidator(0)])

    class Meta:
        unique_together = ("user", "recipe")