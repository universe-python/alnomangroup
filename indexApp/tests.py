from django.test import TestCase
from .models import PropertyPost,Blog

for blog in PropertyPost.objects.all():
    if not blog.slug: 
        blog.save()

for blog in Blog.objects.all():
    if not blog.slug: 
        blog.save()