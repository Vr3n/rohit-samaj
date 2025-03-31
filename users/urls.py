from django.urls import include, path
from users import views


urlpatterns = [
    path('', include('allauth.urls')),
    path('profile/', views.user_profile_view, name="profile")
]
