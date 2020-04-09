from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.models import Count
from django.db.models import Q
from django.urls import reverse
from .models import Recipe, Ingredient, Like, Rating
from .forms import RecipeForm
import operator
from functools import reduce
from django.template.loader import render_to_string
from django.http import JsonResponse


class RecipeCreate(LoginRequiredMixin, generic.CreateView):
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
    model = Recipe
    template_name = 'recipes/index.html'
    paginate_by = 3

    def get_queryset(self):
        ordering = self.get_ordering()
        queryset = Recipe.objects.all()
        query_string = self.request.GET.get('q')
        
        ingredient_keywords_count = 0
        ingredient_queryset =  queryset

        if query_string is not None:
            for term in query_string.split():
                ingredient_queryset = ingredient_queryset.filter(Q(ingredients__name__in=[term.strip()]))
                if ingredient_queryset.exists():
                    ingredient_keywords_count += 1

            if ingredient_keywords_count > 1:
                queryset = ingredient_queryset
            else:               
                lookups = reduce(operator.or_, (  
                            Q(name__icontains=term.strip()) |
                            Q(description__icontains=term.strip()) |
                            Q(ingredients__name__icontains=term.strip()) for term in query_string.split()
                            )
                        )
                
                queryset = queryset.filter(lookups).distinct()
            
        return queryset.order_by('-date_created')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['top_ingredients'] = Ingredient.objects.annotate(recipes_count=Count('recipes')).order_by("-recipes_count")[:5]
        context['recipes_count'] = Recipe.objects.count()
        return context

    
class RecipeDetail(generic.DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['was_liked'] = Like.objects.filter(recipe=self.object, user=self.request.user)
        return context


class RecipeUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/recipe_update.html'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        recipe = self.get_object()
        return self.request.user == recipe.user
    
    def get_success_url(self):
        return reverse('recipes:detail', kwargs={'pk': self.object.pk,})


def like_recipe(request):
    pk = request.POST.get('id')
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user
    like, created = Like.objects.get_or_create(recipe=recipe, user=user)

    if not created:
        like.delete()

    context = {
        'recipe': recipe,
        'was_liked': created
    }
    if request.is_ajax():
        html = render_to_string('recipes/like_template.html', context, request=request)
        return JsonResponse({'form': html})


def rate_recipe(request):
    pk = request.POST.get('id')
    rate = request.POST.get('rate')
    recipe = get_object_or_404(Recipe, pk=pk)
    user = request.user
    rating, created = Rating.objects.get_or_create(recipe=recipe, user=user, defaults={'rate':rate})

    if not created:
        rating.rate = rate
        Rating.objects.filter(recipe=recipe, user=user).update(rate=rate)
    
    # import pdb;pdb.set_trace()
    context = {
        'recipe': recipe,
        'was_rated': created,
        'rate': rate,
    }
    if request.is_ajax():
        html = render_to_string('recipes/rate_template.html', context, request=request)
        return JsonResponse({'form': html})
    