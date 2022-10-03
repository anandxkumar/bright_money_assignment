from django.contrib import admin
from django.conf.urls import url, include


urlpatterns = [
	url(r'^users/', include('users.urls')),
    url(r'^admin/', admin.site.urls),
]
