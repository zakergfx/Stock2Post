from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import requests
from django.contrib.auth.models import User
from . import admanagement
from . import tools

class SendMailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        print(request.data)
        subject = "Prise de contact pour AutoShare"
        body = f'Nom: {request.data["surname"]} {request.data["name"]}\nEntreprise: {request.data["company"]}\
        \nContact: {request.data["phone"]} {request.data["mail"]}\n\nMessage: {request.data["message"]}'

        success = tools.sendMail("zakergfx@gmail.com", subject, body)
        
        return Response({"success": success}, status=200)

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
    
class MeView(APIView):
    def get(self, request):
        return Response({"user": request.user.username}, status=200)
    
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

class TestingView(APIView):
    def post(self, request):
        scenario = request.data["scenario"]
        dealer = models.Dealer.objects.get(fk_user=request.user)

        admanagement.createTestPost(dealer, scenario)

        return Response({dealer.name: scenario}, status=200)
    
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

