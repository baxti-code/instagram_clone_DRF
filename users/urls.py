from .views import CreateUserView, VerifyAPIView, ResendVerifyCodeView, \
    ChangeUserInformationView, ChangeUserPhotoView, LoginView, LoginRefreshView, \
        LogOutView, ForgotPasswordVerifyAPIView, ForgotPasswordView, ResetPasswordAPIView
from django.urls import path

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('login/refresh/', LoginRefreshView.as_view()),
    path('logout/', LogOutView.as_view()),
    path('signup/', CreateUserView.as_view()),
    path('verify/', VerifyAPIView.as_view()),
    path('resend-code/', ResendVerifyCodeView.as_view()),
    path('change-user/', ChangeUserInformationView.as_view()),
    path('change-user-photo/', ChangeUserPhotoView.as_view()),
    path('forgot-password/', ForgotPasswordView.as_view()),
    path('forgot-password/verify/', ForgotPasswordVerifyAPIView.as_view()),
    path('reset-password/', ResetPasswordAPIView.as_view())
]