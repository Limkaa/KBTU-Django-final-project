from django.contrib import admin
from .models import Book, Journal, Profile, User


admin.site.register(Profile)
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Journal)
