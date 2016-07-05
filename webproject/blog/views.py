from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from blog.models import Category, Post
# Create your views here.

def makecategory():
    # 카테고리 구조를 딕셔너리에 담아 반환한다
    tree ={}
    for c1 in Category.objects.filter(level=1).reverse():
        tree[c1]={}
        if c1.under_list() != None:
            for c2 in c1.under_list():
                tree[c1][c2]= list()
                if c2.under_list() != None:
                    for c3 in c2.under_list():
                        tree[c1][c2].append(c3)
    return tree

class Index(TemplateView):
    template_name ='blog/index.html'

    def get_context_data(self, **kwargs):
        context = super(Index,self).get_context_data(**kwargs)
        context['post'] = Post
        context['category'] = makecategory()
        return context

class CategoryList(ListView):
    model = Category
    template_name = 'blog/category.html'

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/postdetail.html'