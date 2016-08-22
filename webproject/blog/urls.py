from django.conf.urls import url,include,patterns
from blog import views

urlpatterns = patterns('',
                       # 인덱스 페이지 (블로그 메인 페이지)
                       url(r'^$',views.Index.as_view(),name='index'),
                       url(r'^category/(?P<name>[a-zA-z0-9가-힣]+)/$',views.CategoryList,name='Category'),
                       url(r'^tag/(?P<name>[a-zA-z0-9가-힣]+)/$',views.TagList,name='Tag'),
                       url(r'^post/(?P<pk>\d+)/$',views.PostDetail.as_view(),name='PostDetail'),
                       )