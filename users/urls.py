from django.urls import include, path
from . import views

app_name = "users"

urlpatterns = [
    path('profile/', views.user_profile_view, name="profile"),
    path('profile/edit-mobile/', views.edit_mobile_number, name="edit_mobile_number"),
    path('profile/update/', views.update_profile, name="update_profile"),
    path('profile/edit-username/', views.edit_username, name="edit_username"),
    path('profile/edit-address/', views.edit_address, name="edit_address"),
    path('profile/update-address/', views.update_address, name="update_address"),
]
