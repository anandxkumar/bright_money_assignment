from django.conf.urls import url
from . import views

app_name = 'users'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^account/profile/(?P<user_id>[0-9]+)/$', views.account_profile, name='account_profile'),
    url(r'^validate/$', views.validate, name='validate'),
    url(r'^invalidate/$', views.invalidate, name='invalidate'),
 	url(r'^register/$', views.register, name='register'),
 	url(r'^getTransactions/$', views.getTransactions, name='getTransactions'),
 	url(r'^getAccounts/$', views.getAccounts, name='getAccounts'),
]
