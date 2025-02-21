from django.urls import path
from . import views  # Importez les vues depuis le fichier views.py

urlpatterns = [

    path("dealers", views.DealersView.as_view()),
    path("dealers/<str:dealer>/", views.DealerSpecificView.as_view()),
    path("dealers/<str:dealer>/settings/", views.SettingsSpecificView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("isregistered/", views.IsRegisteredView.as_view()),
    path("register/", views.RegisterView.as_view())

]