from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from .models import Story, CustomUser, Comment
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .forms import MyUserCreationForm, StoryForm, UserForm, CommentForm
from django.contrib import messages
from django.contrib.auth import authenticate, logout, login, get_user_model
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.urls import reverse




# Create your views here.
def getView(request):

    story = Story.objects.all()
    p = Paginator(story, 5)
    user = request.user
    print(user)

    page_number = request.GET.get("page")
    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(page_number)
    context = {"story_obj": page_obj}
    return render(request, "Horrorify/Home.html", context)


def Searched(request):

    q = request.GET.get("q")
    queryItem = Story.objects.filter(
        Q(title__icontains=q) | Q(author_name__icontains=q)
    )

    p = Paginator(queryItem, 5)

    page_number = request.GET.get("page")

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(page_number)
    context = {"story_obj": page_obj, "q": q}
    return render(request, "Horrorify/Search.html", context)


def Searched(request):

    q = request.GET.get("q")
    queryItem = Story.objects.filter(
        Q(title__icontains=q) | Q(author_name__icontains=q)
    )


    p = Paginator(queryItem, 5)

    page_number = request.GET.get("page")

    try:
        page_obj = p.get_page(page_number)  # returns the desired page object
    except PageNotAnInteger:
        # if page_number is not an integer then assign the first page
        page_obj = p.page(1)
    except EmptyPage:
        # if page is empty then return last page
        page_obj = p.page(page_number)
    context = {"story_obj": page_obj, "q": q}
    return render(request, "Horrorify/Search.html", context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect("home")

    if request.method == "POST":
        email = request.POST.get("email").lower()
        password = request.POST.get("password")

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, "User Does Not Exist.")
            return render(request, "Horrorify/login.html")
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            messages.error(request, "Credentials Don't Match.")
            return render(request, "Horrorify/login.html")

    return render(request, "Horrorify/login.html")


def RegisterUser(request):
    form = MyUserCreationForm()
    if request.method == "POST":
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            # Check if a user with this email already exists
            email = form.cleaned_data.get("email").lower()
            User = get_user_model()

            if User.objects.filter(email=email).exists():
                messages.error(request, "A user with this email already exists.")
                return render(request, "Horrorify/register.html", {"form": form})

            # Create a new user if email is unique
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request=request, user=user)
            return redirect("home")
        else:
            messages.error(request, "An error occurred during registration")

    return render(
        request=request,
        template_name="Horrorify/register.html",
        context={"form": form},
    )


def StoryView(request, pk):
    story = Story.objects.get(id=pk)
    comments = story.comments.all()  # Fetch all comments related to this story
    comment_form = CommentForm()

    return render(
        request=request,
        template_name="Horrorify/Story.html",
        context={
            "story": story,
            "comments": comments,
            "comment_form": comment_form,
        },
    )


@login_required(login_url="Login")
def StoryAdd(request):
    form = StoryForm()
    if request.method == "POST":
        user = request.user
        author_name = user.username
        author_id = user.id
        author_url = f"http://127.0.0.1:8000/profile/{author_id}/"

        CreatedStory = Story.objects.create(
            title=request.POST.get("title"),
            author_name=author_name,
            author=user,
            is_scraped=False,
            author_link=author_url,
            content=request.POST.get("content"),  # Use cleaned_data
        )

        # Use reverse to get the correct URL and redirect
        return redirect(reverse("StoryPage", kwargs={"pk": CreatedStory.id}))
    else:
        form = StoryForm()

    return render(
        request=request,
        template_name="Horrorify/CreateStory.html",
        context={"form": form},
    )


@login_required(login_url="Login")
def UpdateStory(request, pk):
    StoryFind = Story.objects.get(id=pk)
    form = StoryForm(instance=StoryFind)

    if request.user != StoryFind.author:
        return HttpResponse("You are Not allowed!!!")
    if request.method == "POST":
        StoryFind.title = request.POST.get("title")
        StoryFind.content = request.POST.get("content")
        StoryFind.save()
        return redirect("home")
    context = {"form": form, "StoryFind": StoryFind}

    return render(
        request=request,
        template_name="Horrorify/UpdateStory.html",
        context=context,
    )


@login_required(login_url="Login")
def DeleteStory(request, pk):
    StoryFind = Story.objects.get(id=pk)

    if request.user != StoryFind.author:
        return HttpResponse("You are Not allowed!!!")
    if request.method == "POST":
        StoryFind.delete()
        return redirect("home")
    context = {"StoryFind": StoryFind}

    return render(
        request=request,
        template_name="Horrorify/DeleteStory.html",
        context=context,
    )


@login_required(login_url="Login")
def add_comment(request, pk):
    story = get_object_or_404(Story, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.story = story
            comment.save()
            return redirect("StoryPage", pk=story.pk)
    return redirect("StoryPage", pk=story.pk)


@login_required(login_url="Login")
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author and not request.user.is_staff:
        return HttpResponseForbidden("You are not allowed to delete this Comment")

    comment.delete()
    return redirect("StoryPage", pk=comment.story.pk)


@login_required(login_url="Login")
def update_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)

    if request.user != comment.author:
        return HttpResponseForbidden("You are not allowed to delete this Comment")

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect("StoryPage", pk=comment.story.pk)

    else:
        form = CommentForm(instance=comment)

    context = {"form": form, "comment": comment}
    return render(request, "Horrorify/update_comment.html", context)


def UserProfile(request, pk):
    UserFind = CustomUser.objects.get(id=pk)
    UserStory = Story.objects.filter(author=UserFind)

    follower_count = UserFind.followers.count()
    following_count = UserFind.following.count()
    liked_stories = UserFind.liked_stories.all()
    comment = Comment.objects.filter(author=UserFind)

    context = {
        "UserFind": UserFind,
        "UserStory": UserStory,
        "follower_count": follower_count,
        "following_count": following_count,
        "liked_stories": liked_stories,
        "comments":comment
    }

    return render(
        request=request,
        template_name="Horrorify/UserProfile.html",
        context=context,
    )


@login_required(login_url="Login")
def follow_user(request, pk):
    user_to_follow = get_object_or_404(CustomUser, id=pk)
    if request.user != user_to_follow:
        user_to_follow.followers.add(request.user)
    return redirect("Profile", pk=user_to_follow.id)


@login_required(login_url="Login")
def unfollow_user(request, pk):
    user_to_unfollow = get_object_or_404(CustomUser, id=pk)
    if request.user != user_to_unfollow:
        user_to_unfollow.followers.remove(request.user)
    return redirect("Profile", pk=user_to_unfollow.id)


@login_required(login_url="Login")
def like_story(request, story_id):
    user = request.user
    story = get_object_or_404(Story, id=story_id)

    if story in user.liked_stories.all():
        # If the story is already liked, remove it (unlike)
        user.liked_stories.remove(story)
    else:
        # Otherwise, add it to the liked stories
        user.liked_stories.add(story)

    return redirect("StoryPage", pk=story.id)


@login_required(login_url="Login")
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == "POST":
        form = UserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect("Profile", pk=user.id)

    return render(
        request=request,
        template_name="Horrorify/edit-user.html",
        context={"form": form},
    )


def LogoutUser(request):
    logout(request)
    return redirect("home")
