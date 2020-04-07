from django.shortcuts import render, redirect
from django.views import generic
from django.db.models import Count
from django.db.models import Q
from .models import Recipe, Ingredient
from .forms import RecipeForm


class RecipeCreate(generic.CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_form.html'

    def get(self, request):
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
    template_name = 'recipes/index.html'

    def get_queryset(self):
        queryset = Recipe.objects.all()
        query_string = self.request.GET.get('q')

        if query_string is not None:
            queryset = queryset.filter(Q(name__icontains=query_string) | Q(description__icontains=query_string))

        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_ingredients'] = Ingredient.objects.annotate(recipes_count=Count('recipes')).order_by("-recipes_count")[:5]
        return context

    
class RecipeDetail(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'

