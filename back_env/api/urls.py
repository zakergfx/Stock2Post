from django.urls import path
from . import views  # Importez les vues depuis le fichier views.py

urlpatterns = [

    path("tempmakes/", views.tempMakesView.as_view()),
    path("makes/", views.MakesView.as_view()),
    path("models/", views.ModelsView.as_view()),

    path("dealers/", views.DealersView.as_view()),
    path("me/", views.MeView.as_view()),
    path("requeststatus/", views.RequestStatusView.as_view()),
    path("sendmail/", views.SendMailView.as_view()),
    path("dealers/<str:dealer>/", views.DealerSpecificView.as_view()),
    path("dealers/<str:dealer>/settings/", views.SettingsSpecificView.as_view()),
    path("login/", views.LoginView.as_view()),
    path("facebooklink/", views.FacebookLinkView.as_view()),
    path("instagramlink/", views.InstagramLinkView.as_view()),
    path("testing/", views.TestingView.as_view())

]