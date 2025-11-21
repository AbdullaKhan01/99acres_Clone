from django.contrib import admin
from django.urls import path, include
from listings import views as listing_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', listing_views.home, name='home'),
    path('listings/', listing_views.all_listings, name='all_listings'), 
    path('property/<int:pk>/', listing_views.property_detail, name='property_detail'),
    path('property/<int:pk>/edit/', listing_views.edit_property, name='edit_property'),
    path('add-property/', listing_views.add_property, name='add_property'),
    path('search/', listing_views.search, name='search'),
    path('my-listings/', listing_views.my_listings, name='my_listings'),
    path('register/', listing_views.register_view, name='register'),
    path('login/', listing_views.login_view, name='login'),
    path('logout/', listing_views.logout_view, name='logout'),
]
