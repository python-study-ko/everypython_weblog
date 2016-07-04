from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from blog.models import Category, Post
# Create your views here.
def category_level():
    """
    카테고리의 레벨별로 딕셔너리에 분류해주는 함수/ 카테고뢰 목록구현에 사용한다.
    :return: {1:['a','b','c'],2:['d','e'],3:['x','z']}
    """
    for Category

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