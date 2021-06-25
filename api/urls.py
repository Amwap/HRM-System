from django.urls import path
from . import views

urlpatterns = [
    path('', views.Main.as_view()),
    path('login', views.Login.as_view()),
    path('registration', views.Registration.as_view()),
    # path('verify', views.MailVerify.as_view()),
    path('autorization', views.Autorization.as_view()),
    path('api', views.Api.as_view())

    # path('api/', views.Gateway.as_view()),
    # path('api/gettable/', views.FillTable.as_view()),
    # path('', views.Page.as_view())
]