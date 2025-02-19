from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
import requests

class DealerSpecificView(APIView):
    def get(self, request, dealer):
        dealer = models.Dealer.objects.get(name=dealer)
        serializer = serializers.DealerSerializer(dealer)
        return Response(serializer.data, status=200)
    
class SettingsSpecificView(APIView):
    def patch(self, request, dealer):
        dealer = models.Dealer.objects.get(name=dealer)
        currentSettings = dealer.fk_settings
        newSettings = request.data
        
        for key, value in newSettings.items():
            setattr(currentSettings, key, value)

        currentSettings.save()

        return Response(newSettings, status=200)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        # récupérer token de fb et faire le lien
        token = request.data["token"]

        url = "https://graph.facebook.com/v22.0/me"
        response = requests.get(url, headers={"Authorization": f"OAuth {token}"}).json()

        dealer = models.Dealer.objects.filter(fbId=None)

        if len(dealer) > 0: # si premiere connexion
            dealer = dealer[0]
            dealer.fbId = response["id"]
            dealer.save()

        else: # si pas premiere connexion
            dealer = models.Dealer.objects.get(fbId = response["id"])


        refresh = RefreshToken.for_user(dealer.fk_user)
        return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                },
                status=200
            )