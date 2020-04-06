from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import Recipe, Ingredient
from .forms import RecipeForm
from django.views import generic

class RecipeCreate(CreateView):
    
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get(self,request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            recipe = form.save(commit=False)
            recipe.user = self.request.user
            recipe.save()
            form.save_m2m()
            return redirect('recipes:index')
        return render(request, self.template_name, {'form': form})

class IndexView(generic.ListView):

    template_name =  'recipes/index.html'

    def get_queryset(self):
        return Recipe.objects.all()


class RecipeDetail(generic.DetailView):
    model = Recipe
    template_name =  'recipes/recipe_detail.html'

