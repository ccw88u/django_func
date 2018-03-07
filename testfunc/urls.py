
from django.conf.urls import url
from testfunc import views
from django.conf.urls import include


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^setcookienumber$', views.setcookienumber, name='setcookienumber'),
    url(r'^setsession$', views.setsession, name='setsession'),
    url(r'^languagedisp$', views.languagedisp, name='languagedisp'),
    url(r'^memorycachetest$', views.memorycachetest, name='memorycachetest'),
    url(r'^newspage$', views.newspage, name='newspage'),
]


