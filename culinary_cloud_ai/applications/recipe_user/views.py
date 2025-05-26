from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from applications.recipe_user.forms import RecipeUserRegistrationForm, RecipeUserUpdateForm
from django.contrib import messages


# Create your views here.

def recipeuserLogin(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            recipe_username = form.cleaned_data.get("username")
            recipe_userpass = form.cleaned_data.get("password")

            recipe_user = authenticate(request, username=recipe_username, password=recipe_userpass)
            if recipe_user is not None:

                login(request, recipe_user)

                return redirect('recipes:home')
            else:
                print("Authentication failed!")
                return redirect('login')
    else:
        form = AuthenticationForm()

    return render(request, "recipe_user/recipeuser_login.html", {'form': form})

def recipeuserLogout(request):
    logout(request)     
    return redirect('login')

def recipeuserRegister(request):
    if request.method == "POST":
        form = RecipeUserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Registration Successful!! You can log-in now")
            return redirect("login")
        else:
            messages.error(request, 'There were errors in your form. Please fix them below.')
            return render(request, "recipe_user/recipeuser_register.html", {"form": form})
    else:
        form = RecipeUserRegistrationForm()
        return render(request, "recipe_user/recipeuser_register.html", {"form": form})

@login_required    
def recipeuserDetails(request):
    recipeuser = request.user
    return render(request, "recipe_user/recipeuser_details.html", {"recipeuser": recipeuser})

@login_required
def recipeuserUpdate(request):
    recipeuser = request.user
    if request.method == "POST":
        form = RecipeUserUpdateForm(request.POST, request.FILES, instance=recipeuser)
        if form.is_valid():
            form.save()
            messages.success(request, "Updated Profile Successfully!!")
            return redirect("profile")
        else:
            messages.error(request, "There were errors in your form. Please fix them below.")
            return render(request, "recipe_user/recipeuser_update.html", {"form": form})
    else:
        form = RecipeUserUpdateForm(instance=recipeuser)
        return render(request, "recipe_user/recipeuser_update.html", {"form": form})