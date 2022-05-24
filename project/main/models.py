from django.db import models

from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.models import AbstractBaseUser

from .managers import UserManager

class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, blank=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self) -> str:
        return self.email


class Profile(models.Model):
    """ Profile with additional info for User instance (One to one) """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    bio = models.TextField(max_length=500, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Profile'
        verbose_name_plural = 'Profiles'
    
    def __str__(self) -> str:
        return str(self.user)


class BookJournalBase(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False)
    price = models.PositiveIntegerField(default=0, null=False, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Book(BookJournalBase):
    num_pages = models.PositiveIntegerField(default=0, null=False, blank=False)
    genre = models.CharField(max_length=300, null=False, blank=False)
    
    class Meta:
        verbose_name = 'Book'
        verbose_name_plural = 'Books'
        

class Journal(BookJournalBase):
    BULLET = 1
    FOOD = 2
    TRAVEL = 3
    SPORT = 4
    
    TYPE_CHOICES = [
        (BULLET, 'Bullet'),
        (FOOD, 'Food'),
        (TRAVEL, 'Travel'),
        (SPORT, 'Sport'),
    ]
    
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=BULLET)
    publisher = models.CharField(max_length=300, null=False, blank=False)
    
    class Meta:
        verbose_name = 'Journal'
        verbose_name_plural = 'Journals'

    def __str__(self):
        return f'{self.name} ({self.publisher})'
    