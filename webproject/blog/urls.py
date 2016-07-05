from django.conf.urls import url,include,patterns
from blog import views

urlpatterns = patterns('',
                       # 인덱스 페이지 (블로그 메인 페이지)
                       url(r'^$',views.Index.as_view(),name='index'),
                       url(r'^category/(?P<pk>\d+)/$',views.CategoryList.as_view(),name='CategoryList'),
                       url(r'^post/(?P<pk>\d+)/$',views.PostDetail.as_view(),name='PostDetail'),
                       )