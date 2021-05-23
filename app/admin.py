from django.contrib import admin
from .models import User, Post, Location, Comment, Like, Notification

# Register your models here.

admin.site.register(User)
admin.site.register(Post)
admin.site.register(Location)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Notification)
