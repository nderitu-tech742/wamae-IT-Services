from django.contrib import admin
from django.urls import path, include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('our_services.urls')),
    path('payments/', include('payments.urls')),
]
 
from our_services.home_redirect import home_redirect_view 
urlpatterns.append(path('', home_redirect_view)) 
 
from our_services.home_redirect import home_redirect_view 
from django.urls import path 
urlpatterns.append(path('', home_redirect_view)) 
 
from our_services.home_redirect import home_redirect_view 
from django.urls import path 
urlpatterns.append(path('', home_redirect_view)) 
 
from our_services.home import home 
urlpatterns.append(path('', home, name='home')) 
 
from our_services.home import home 
urlpatterns.append(path('', home, name='home')) 
 
from our_services.home import home 
urlpatterns.append(path('', home, name='home')) 
from our_services.index_view import index 
urlpatterns.append(path('', index, name='index')) 
from our_services.index_view import index 
from django.urls import path 
urlpatterns.append(path('', index, name='index')) 
