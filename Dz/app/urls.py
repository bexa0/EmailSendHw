from django.urls import path

from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.LoginForm.as_view(), name='login'),
    path('register/', views.SignUp.as_view(), name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('enter_your_login/', views.enter_your_ligin, name='eyl'),
    path('repassword/<str:username>', views.repassword, name='repassword'),
    path('send_key/<str:username>', views.send_message, name='send_message'),
    path('/confrim_page/<str:username>', views.confrim_page, name='confirm_page'),
    path('error/', views.some_error_occurred, name='some_error_occurred')
]