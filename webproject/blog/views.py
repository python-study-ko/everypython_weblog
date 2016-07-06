from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic.base import TemplateView
from blog.models import Category, Post

from django_jinja.views.generic.detail import DetailView

# Create your views here.


class Index(TemplateView):
    template_name ='blog/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index,self).get_context_data(**kwargs)
        context['post'] = Post
        context['category'] = Category
        return context

class CategoryList(ListView):
    model = Category
    template_name = 'blog/category.html'

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/postdetail.html'

# jinja2 테스트 코드
def jinjadef(request):
    test = 'abcd'
    manydict = {1:{"first":1,"second":2,"tree":{3:33}}}
    return render(request,'blog/def.jinja',{'hi' :test,"test":manydict})

class jinjaclass(DetailView):
    model = Post

