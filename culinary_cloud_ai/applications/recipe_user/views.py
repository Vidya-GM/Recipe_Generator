from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from applications.recipe_user.forms import RecipeUserRegistrationForm, RecipeUserUpdateForm
from django.contrib import messages
from applications.recipe_user.models import Notification
from django.db.models import Q, Count, Exists, OuterRef
from applications.recipes.models import Recipe, Like, Comment


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


@login_required
def myRecipes(request):
    recipeuser = request.user
    my_recipes = recipeuser.recipe_set.all()
    print(my_recipes)
    return render(request, "recipe_user/my_recipe_list.html", {"my_recipes": my_recipes,
                                                            "recipeuser": recipeuser})


@login_required
def notificationList(request):
    notifications = request.user.notifications.all()
    notif_recipient = request.user
    return render(request, "recipe_user/notification_list.html", {"notifications": notifications,
                                                                    "notif_recipient": notif_recipient})


@login_required
def notificationVisit(request, pk):
    notification = get_object_or_404(Notification, pk=pk, notif_recipient=request.user)
    notification.is_read = True
    notification.save()

    target = notification.target

    # If target is a Comment or Like, redirect to its recipe
    if hasattr(target, 'recipe'):
        # If it's a Comment, include anchor to scroll to it
        if target.__class__.__name__ == "Comment":
            return redirect(f"{target.recipe.get_absolute_url()}#comment-{target.id}")
        elif target.__class__.__name__ == "Like":
            return redirect(f"{target.recipe.get_absolute_url()}#likes") 

        return redirect(target.recipe.get_absolute_url())

    # If it's a Recipe
    if hasattr(target, 'get_absolute_url'):
        return redirect(target.get_absolute_url())

    # Fallback
    return redirect("notifications-list")


@login_required
def delete_selected_notification(request):
    if request.method == "POST":
        ids = request.POST.getlist("selected_notifications")
        Notification.objects.filter(id__in=ids, notif_recipient=request.user).delete()
    return redirect("notification-list")


@login_required
def myRecipes(request):
    recipeuser = request.user
    queryset = Recipe.objects.filter(recipe_owner=recipeuser)

    q = request.GET.get("q")
    if q:
        queryset = queryset.filter(
            Q(title__icontains=q) |
            Q(description__icontains=q) |
            Q(ingredients__icontains=q)
        )

    queryset = queryset.annotate(
        likes_count=Count('likes', distinct=True),
        annotated_comments_count=Count('comments', distinct=True)
    )

    if recipeuser.is_authenticated:
        user_likes = Like.objects.filter(author=recipeuser, recipe=OuterRef('pk'))
        queryset = queryset.annotate(user_liked=Exists(user_likes))
    else:
        queryset = queryset.annotate(user_liked=Q(pk__isnull=True))

    sort_option = request.GET.get("sort", "-created_at")
    allowed_sorts = ["-created_at", "created_at", "-likes_count", "-annotated_comments_count"]

    if sort_option in allowed_sorts:
        queryset = queryset.order_by(sort_option)
    else:
        queryset = queryset.order_by("-created_at")

    return render(request, "recipe_user/my_recipe_list.html", {
        "my_recipes": queryset,
        "recipeuser": recipeuser,
    })