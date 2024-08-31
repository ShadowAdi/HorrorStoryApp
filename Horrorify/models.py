from django.core.exceptions import ValidationError
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.conf import settings


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a user with an email and password.
        """
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser with the given email and password.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)





class Story(models.Model):
    title = models.CharField(max_length=255)
    author_name = models.CharField(
        max_length=255, blank=True, null=True
    )  # For scraped stories
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True
    )
    author_link = models.URLField(
        blank=True, null=True
    )  # Link to the author's profile or story source
    content = models.TextField()
    is_scraped = models.BooleanField(
        default=False
    )  # Flag to indicate if the story was scraped or user-created
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.is_scraped:
            if self.author is not None:
                raise ValidationError(
                    "Scraped stories should not have an associated user."
                )
            if not self.author_name:
                raise ValidationError("Scraped stories must have an author name.")
        else:
            if self.author is None:
                raise ValidationError(
                    "User-created stories must have an associated user."
                )

    def __str__(self):
        return self.title


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    bio = models.TextField(blank=True)
    followers = models.ManyToManyField(
        "self", symmetrical=False, related_name="following", blank=True
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    liked_stories = models.ManyToManyField(
        Story, related_name="liked_by_users", blank=True
    )  # New field to track liked stories

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

class Comment(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Comment by {self.author.username} on {self.story.title}'


