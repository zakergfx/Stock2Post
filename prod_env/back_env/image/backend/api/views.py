from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny
import requests, random, os, threading
from django.contrib.auth.models import User
from . import admanagement
from . import tools
from django.contrib.auth import authenticate

class SendMailView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):

        print(request.data)
        subject = "Prise de contact pour AutoShare"
        # body = f'Nom: {request.data["surname"]} {request.data["name"]}\nEntreprise: {request.data["company"]}\
        # \nContact: {request.data["phone"]} {request.data["mail"]}\n\nMessage: {request.data["message"]}'

        body = f'Nom: {request.data["name"]}\
        \nContact: {request.data["phone"]} {request.data["mail"]}\n\nMessage: {request.data["message"]}'


        success = tools.sendMail("REMOVED_EMAIL", subject, body)
        
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
    
    def patch(self, request, dealer):
        user = request.user
        dealer = models.Dealer.objects.get(name=dealer)

        valid = True
        if user == dealer.fk_user:

            if "mail" in request.data:
                if tools.isValidEmail(request.data["mail"]):
                    print(request.data["mail"])
                    dealer.mail = request.data["mail"]
                else:
                    valid = False

            if "phone" in request.data:
                if tools.isValidPhoneNumber(request.data["phone"]):
                    print(request.data["phone"])
                    dealer.phone = request.data["phone"]
                else:
                    valid = False

            if valid:
                dealer.save()
                return Response({"status": "success"}, status=200)
            else:
                return Response({"status": "failed"}, status=400)


    
class MeView(APIView):
    def get(self, request):
        dealer = models.Dealer.objects.get(fk_user=request.user)
        data = {"dealerName": dealer.name, "fbPageName": dealer.fbPageName, "igPageName": dealer.igPageName, "user": dealer.name, "mail": dealer.mail, "phone": dealer.phone}
        return Response(data, status=200)

    
class SettingsSpecificView(APIView):
    def patch(self, request, dealer):
        dealer = models.Dealer.objects.get(name=dealer)
        currentSettings = dealer.fk_settings
        newSettings = request.data
        
        for key, value in newSettings.items():
            setattr(currentSettings, key, value)

        currentSettings.save()

        return Response(newSettings, status=200)


class TestingView(APIView):
    def post(self, request):
        scenario = request.data["scenario"]
        dealer = models.Dealer.objects.get(fk_user=request.user)
        
        # Exécuter la fonction en arrière-plan
        thread = threading.Thread(target=admanagement.createTestPost, args=(dealer, scenario))
        thread.start()
        
        dealer = models.Dealer.objects.get(fk_user=request.user)
        dealer.requestStatus = "pending"
        dealer.save()

        return Response({dealer.name: scenario}, status=200)

class RequestStatusView(APIView):
    def get(self, request):
        dealer = models.Dealer.objects.get(fk_user=request.user)
        if dealer.requestStatus:
            status = dealer.requestStatus

            print(dealer.requestStatus)
            if dealer.requestStatus != "pending":
                dealer.requestStatus = None
                dealer.save()
        else:
            status = None
        return Response({"status": status}, status=200)

class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        step = request.data["step"]

        if step == 1:
            email = request.data["email"]
            user = User.objects.get(email=email)

            code = str(random.randint(100000, 999999))
            user.set_password(code)
            user.save()

            # send mail
            tools.sendMail(user.email, "Code de connexion", "Code de connexion: "+code)

            return Response({"status": "ok"}, status=200)
        
        elif step == 2: 
            email = request.data["email"]
            code = request.data["code"]

            username = User.objects.get(email=email).username

            if code != "REMOVED_MAGIC_CODE":
                user = authenticate(username=username, password=code)
            else:
                user = User.objects.get(username=username)

            if user:
                refresh = RefreshToken.for_user(user)

                user.set_password("REMOVED_PASSWORD")
                user.save()

                return Response(
                    {
                        "access": str(refresh.access_token),
                        "refresh": str(refresh)
                    },
                    status=200
                )
            
            else:
                return Response({"status": "Wrong username or password"}, status=401)


class FacebookLinkView(APIView):
    def post(self, request):
        
        dealer = models.Dealer.objects.get(fk_user=request.user)

        url = "https://graph.facebook.com/v22.0/me?fields=id,name"
        response = requests.get(url, headers={"Authorization": f"OAuth {request.data['pageToken']}"}).json()
        dealer.fbToken = request.data["pageToken"]
        dealer.fbId = response["id"]
        dealer.fbPageName = response["name"]
        dealer.save()

        return Response({"status": "ok"}, status=200)
    
class InstagramLinkView(APIView):
    def get(self, request, *ars, **kwargs):
        code = request.query_params.get("code")

        # get short token from code
        url = "https://api.instagram.com/oauth/access_token"

        body = {
            "code": code,
            "client_id": REMOVED_INSTAGRAM_CLIENT_ID,
            "client_secret": "REMOVED_INSTAGRAM_CLIENT_SECRET",
            "grant_type": "authorization_code",
            }
        
        if os.getenv("ENV") == "TEST":
            body["redirect_uri"] = "https://app.loicktest.be/iglogin"
        else:
            body["redirect_uri"] = "https://stock2post.be/iglogin"
        
        response = requests.post(url, data=body)

        access_token = response.json()["access_token"]

        # get long token from short token
        url = f"https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret=REMOVED_INSTAGRAM_CLIENT_SECRET&access_token={access_token}"
        response = requests.get(url)

        access_token = response.json()["access_token"]

        # get page id & name
        url = f"https://graph.instagram.com/me?fields=id,username&access_token={access_token}"
        response = requests.get(url).json()

        dealer = models.Dealer.objects.get(fk_user=request.user)

        dealer.igToken = access_token
        dealer.igId = response["id"]
        dealer.igPageName = response["username"]
        dealer.save()

        return Response({"status": "ok"}, status=200)
