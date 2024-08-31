from django.forms import ModelForm
from .models import Story, CustomUser, Comment
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


User = get_user_model()


class MyUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data.get("email").lower()
        if User.objects.filter(email=email).exists():
            raise ValidationError("A user with this email already exists.")
        return email


class StoryForm(ModelForm):
    class Meta:
        model = Story
        fields = "__all__"
        widgets = {
            "title": forms.TextInput(
                attrs={
                    "class": "w-full p-2 border border-gray-300 text-black rounded focus:outline-none focus:ring-2 focus:ring-[#221d33]",
                    "placeholder": "Enter story title",
                }
            ),
            "content": forms.Textarea(
                attrs={
                    "class": "w-full p-2 border border-gray-300 text-black pb-2 rounded overflow-hidden focus:outline-none focus:ring-2 focus:ring-[#221d33]",
                    "placeholder": "Enter story content",
                }
            ),
        }


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "avatar", "bio"]
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "class": "w-full p-2 border border-gray-300 text-black rounded focus:outline-none focus:ring-2 focus:ring-[#221d33]",
                    "placeholder": "Enter username",
                }
            ),
            "email": forms.EmailInput(
                attrs={
                    "class": "w-full p-2 border border-gray-300 text-black rounded focus:outline-none focus:ring-2 focus:ring-[#221d33]",
                    "placeholder": "Enter email address",
                }
            ),
            "bio": forms.Textarea(
                attrs={
                    "class": "w-full p-2 border border-gray-300 text-black rounded focus:outline-none focus:ring-2 focus:ring-[#221d33]",
                    "placeholder": "Enter a short bio",
                }
            ),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={
                    "class": "w-full text-black p-2 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:border-gray-800",
                    "rows": 2,
                    "placeholder": "Enter Your Thoughts...",
                }
            ),
        }
