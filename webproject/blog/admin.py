from django.contrib import admin
from blog.models import Category, Post, OrderCategory



admin.site.register(Category)
admin.site.register(OrderCategory)
admin.site.register(Post)