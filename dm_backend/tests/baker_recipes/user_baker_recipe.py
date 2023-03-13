# TODO: fix this when we have a user model
from django.contrib.auth.models import User
from model_bakery.recipe import Recipe

user_recipe = Recipe(User)
