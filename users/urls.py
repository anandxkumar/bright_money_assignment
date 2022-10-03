from django.conf.urls import url
from . import views

app_name = 'users'
from django.urls import path  

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^success_loggin/(?P<user_id>[0-9]+)/$', views.success_loggin, name='success_loggin'),
    url(r'^validate/$', views.validate, name='validate'),
    url(r'^invalidate/$', views.invalidate, name='invalidate'),
 	url(r'^register/$', views.register, name='register'),
 	url(r'^getTransactions/$', views.getTransactions, name='getTransactions'),
 	url(r'^getAccounts/$', views.getAccounts, name='getAccounts'),
    url(r'^getTotalTransactions/$', views.getTotalTransactions, name='getTotalTransactions'),
    url(r'^getAccountsCelery/$', views.testCelery, name='getAccountsCelery'),  
]
