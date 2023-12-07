from django.urls import path
from api.views import UserRegistration,UserLoginView,UserProfileView,ChangePasswordView,ResetEmailView,ResetPasswordView

urlpatterns = [
    path('registration/',UserRegistration.as_view()),
    path('login/',UserLoginView.as_view()),
    path('profile/',UserProfileView.as_view()), 
    path('changepassword/',ChangePasswordView.as_view()),
    path('resetemail/',ResetEmailView.as_view()),
    path('resetpassword/<uid>/<token>/',ResetPasswordView.as_view())
    
    
]
