from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from saved_recipes.models import SavedRecipe
from django.contrib.auth.decorators import login_required
from .forms import ExtendedCreationForm, AccountEditForm

class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = ExtendedCreationForm
    success_url = reverse_lazy ("login")

    def register(request):
        if request.method == 'POST':
            form = ExtendedCreationForm(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('home')
        else:
            form  = ExtendedCreationForm()

        return render(request, "registration/signup.html", {'form': form})

@login_required
def account_info_view(request):
    user = request.user
    saved_recipe_count = SavedRecipe.objects.filter(user=user).count()
    context = {
        'user': user,
        'saved_recipes_count': saved_recipe_count,
    }
    return render(request, 'accounts/account_info.html', context)

@login_required
def edit_account(request):
    if request.method == 'POST':
        form = AccountEditForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account_info')
    else:
        form = AccountEditForm(instance=request.user)

    return render(request, 'accounts/edit_account.html', {'form': form})

