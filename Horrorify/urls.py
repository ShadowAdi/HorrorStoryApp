from django.urls import path,include
from . import views


urlpatterns = [
    path("", views.getView, name="home"),
    path("Seach/", views.Searched, name="Search"),
    path("register/", views.RegisterUser, name="Register"),
    path("login/", views.login_page, name="Login"),
    path("logout/", views.LogoutUser, name="Logout"),
    path("story/<str:pk>", views.StoryView, name="StoryPage"),
    path("create-story/", views.StoryAdd, name="CreateStory"),
    path("update-story/<str:pk>", views.UpdateStory, name="UpdateStory"),
    path("delete-story/<str:pk>", views.DeleteStory, name="DeleteStory"),
    path("profile/<str:pk>", views.UserProfile, name="Profile"),
    path("follow/<str:pk>", views.follow_user, name="FollowUser"),  # New follow URL
    path("unfollow/<str:pk>", views.unfollow_user, name="UnfollowUser"),
    path("like-story/<int:story_id>/", views.like_story, name="like_story"),
    path("edit-User/", views.updateUser, name="updateUser"),
    path("story/<int:pk>/add_comment/", views.add_comment, name="add_comment"),
    path("comment/delete/<int:pk>/", views.delete_comment, name="delete_comment"),
    path("comment/update/<int:pk>/", views.update_comment, name="update_comment"),
]

