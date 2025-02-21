from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
import requests
from django.contrib.auth import login
from django.contrib.auth.models import User

class DealersView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def get(self, request):
        dealers = models.Dealer.objects.filter(fk_user=None)
        serializer = serializers.DealerSerializer(dealers, many=True)
        return Response(serializer.data, status=200)

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

class IsRegisteredView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        # récupérer token de fb et faire le lien
        token = request.data["token"]

        url = "https://graph.facebook.com/v22.0/me"
        response = requests.get(url, headers={"Authorization": f"OAuth {token}"}).json()

        fbId = response["id"]
        
        accountExists = len(models.Dealer.objects.filter(fbId=fbId)) > 0

        data = {"isRegistered": accountExists}
        return Response(data, status=200)

class RegisterView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        user = User.objects.create_user(username=request.data["dealer"], password="Fmei&W2@GAvHKru4ZfR3")
        user.save()

        dealer = models.Dealer.objects.get(name=request.data["dealer"])
        dealer.fk_user = user
        dealer.token = request.data["pageToken"]
        dealer.fbId = request.data["fbId"]
        dealer.save()

        return Response({"success": True}, status=200)


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        # récupérer token de fb et faire le lien
        token = request.data["token"]

        url = "https://graph.facebook.com/v22.0/me"
        response = requests.get(url, headers={"Authorization": f"OAuth {token}"}).json()

        fbId = response["id"]

        dealer = models.Dealer.objects.get(fbId=fbId)
        
        refresh = RefreshToken.for_user(dealer.fk_user)
        return Response(
                {
                    "access": str(refresh.access_token),
                    "refresh": str(refresh)
                },
                status=200
            )

