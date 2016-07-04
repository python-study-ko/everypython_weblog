from django.conf.urls import url,patterns
from testboot import views

urlpatterns = patterns("",
                       url(r'^$',views.index,name='index'),
                       )