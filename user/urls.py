from django.urls import path
from user import views


urlpatterns = [
    path('profile', view=views.ProfileAPIs.as_view()),
    path('profile/change_password', view=views.ChangePasswordAPI.as_view()),
    path('profile/signup', view=views.SignUpAPI.as_view())
]