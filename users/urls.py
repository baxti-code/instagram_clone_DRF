from .views import CreateUserView, VerifyAPIView, ResendVerifyCodeView, \
    ChangeUserInformationView, ChangeUserPhotoView, LoginView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('resend-code/', ResendVerifyCodeView.as_view()),
    path('change-user/', ChangeUserInformationView.as_view()),
    path('change-user-photo/', ChangeUserPhotoView.as_view())
]