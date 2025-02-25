import requests, time, json
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from . import models, tools
from difflib import SequenceMatcher
import hashlib
import cv2
import numpy as np

BASEURL = f"https://graph.facebook.com/v22.0"

def testing():
    # scheduledTask()
    createVideo()




def cleanFbPage():
    dealers = models.Dealer.objects.all()
    for dealer in dealers:
        url = f"{BASEURL}/{dealer.fbId}/feed"
        headers = {"Authorization": f"OAuth {dealer.token}"}
        response = requests.get(url, headers=headers).json()

        
        for line in response:
            url = f"{BASEURL}/{dealer.fbId}_{line['id'].split('_')[1]}"
            response = requests.delete(url, headers=headers)

        print("suppression ok")


def createVideo():
    images = ["media/modifiedFile.jpg", "media/originalFile.jpg"]
   # Paramètres de la vidéo
    fps = 1  # Images par seconde
    duration_per_image = 3  # Durée d'affichage de chaque image (en secondes)
    frame_size = (640, 480)  # Taille de la vidéo
    output_file = "diaporama.avi"

    # Création du writer vidéo
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    video = cv2.VideoWriter(output_file, fourcc, fps, frame_size)

    for image_path in images:
        img = cv2.imread(image_path)
        
        if img is None:
            print(f"Erreur : Impossible de charger {image_path}")
            continue
        
        img = cv2.resize(img, frame_size)  # Redimensionner l'image
        
        # Ajouter du texte "test" au centre
        font = cv2.FONT_HERSHEY_SIMPLEX
        text = "test"
        font_scale = 2
        font_thickness = 5
        text_color = (255, 255, 255)  # Blanc
        outline_color = (0, 0, 0)  # Noir

        # Obtenir la taille du texte pour le centrer
        text_size = cv2.getTextSize(text, font, font_scale, font_thickness)[0]
        text_x = (frame_size[0] - text_size[0]) // 2
        text_y = (frame_size[1] + text_size[1]) // 2

        # Ajouter un contour noir pour la lisibilité
        for dx, dy in [(-2, -2), (-2, 2), (2, -2), (2, 2)]:  # 4 coins autour du texte
            cv2.putText(img, text, (text_x + dx, text_y + dy), font, font_scale, outline_color, font_thickness)

        # Ajouter le texte en blanc
        cv2.putText(img, text, (text_x, text_y), font, font_scale, text_color, font_thickness)

        # Ajouter plusieurs copies de l'image pour créer un effet de pause
        for _ in range(fps * duration_per_image):
            video.write(img)

    video.release()
    cv2.destroyAllWindows()

    print(f"Vidéo créée avec succès : {output_file}")


def addImageToImage(imagePath, overlayPath, outputPath, position=None):
    # Ouvre les images
    baseImage = Image.open(imagePath).convert("RGBA")
    overlayImage = Image.open(overlayPath,).convert("RGBA")
    
    # Calcule le ratio pour redimensionner l'image de superposition sans la déformer
    overlayRatio = min(baseImage.width / overlayImage.width, baseImage.height / overlayImage.height)
    newSize = (int(1.5*overlayImage.width * overlayRatio)//2, int(1.5*overlayImage.height * overlayRatio)//2)
    overlayImage = overlayImage.resize(newSize, Image.LANCZOS)
    
    # Définit la position par défaut (centrée si non spécifiée)
    if position is None:
        position = ((baseImage.width - overlayImage.width) // 2, 
                    (baseImage.height - overlayImage.height) // 2)
    
    # Superpose les images
    baseImage.paste(overlayImage, position, overlayImage)
    
    # Sauvegarde l'image finale
    baseImage.save(outputPath, "PNG")

def objToDict(obj):
    return {field.name: getattr(obj, field.name) for field in obj._meta.fields}

def dictToHash(d, keys):
    content = ""
    for key in keys:
        if key in d:
            if d[key] is not None:
                content += f"{key}:{d[key]}"
        
    return hashlib.sha256(content.encode()).hexdigest()

def createSoldPicture(ad):
    data = requests.get(ad.mainPicture).content
    with open ("media/originalFile.jpg", "wb") as f:
        f.write(data)

    addImageToImage("media/originalFile.jpg","media/sold.png" , "media/modifiedFile.jpg")


def isTimestampOlderThan(weeks, timestamp):
    timestampDate = datetime.fromtimestamp(timestamp)
    oneMonthAgo = datetime.now() - timedelta(days=weeks*7)
    
    return timestampDate < oneMonthAgo

def formatNumber(number):
    return f"{number:,}".replace(",", " ")

def boldText(text):
    boldLetters = {
        'a': '𝗮', 'b': '𝗯', 'c': '𝗰', 'd': '𝗱', 'e': '𝗲', 'f': '𝗳', 'g': '𝗴', 'h': '𝗵', 'i': '𝗶', 'j': '𝗷', 'k': '𝗸',
        'l': '𝗹', 'm': '𝗺', 'n': '𝗻', 'o': '𝗼', 'p': '𝗽', 'q': '𝗾', 'r': '𝗿', 's': '𝘀', 't': '𝘁', 'u': '𝘂', 'v': '𝘃',
        'w': '𝘄', 'x': '𝘅', 'y': '𝘆', 'z': '𝘇',
        'A': '𝗔', 'B': '𝗕', 'C': '𝗖', 'D': '𝗗', 'E': '𝗘', 'F': '𝗙', 'G': '𝗚', 'H': '𝗛', 'I': '𝗜', 'J': '𝗝', 'K': '𝗞',
        'L': '𝗟', 'M': '𝗠', 'N': '𝗡', 'O': '𝗢', 'P': '𝗣', 'Q': '𝗤', 'R': '𝗥', 'S': '𝗦', 'T': '𝗧', 'U': '𝗨', 'V': '𝗩',
        'W': '𝗪', 'X': '𝗫', 'Y': '𝗬', 'Z': '𝗭',
        '0': '𝟬', '1': '𝟭', '2': '𝟮', '3': '𝟯', '4': '𝟰', '5': '𝟱', '6': '𝟲', '7': '𝟳', '8': '𝟴', '9': '𝟵'
    }
    
    boldedText = "".join(boldLetters.get(char, char) for char in str(text))
    return boldedText


def isAdInDb(url):
    inDb = models.Ad.objects.filter(url=url).exists()
    return inDb

def getDealerLocalAds(dealer):
    ads = models.Ad.objects.filter(fk_dealer__name=dealer)
    return ads

def getDynamicPageHtml(url):
    # Configuration du navigateur sans interface graphique (headless)
    options = Options()
    options.add_argument("--headless")  # Exécute Chrome en arrière-plan
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

    # Lancement du navigateur
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    driver.get(url)
    return driver.page_source


def getParsedHtmlTab(soup, idName):
    basicData = soup.find(id=idName)
    keys = basicData.find_all("dt")
    values = basicData.find_all("dd")
    tempDict = {}

    for key, value in zip(keys, values):
        tempDict[key.get_text()] = value.get_text().replace("\u202f", " ")
    return tempDict

def setEquipment(soup, sep="\n"):
    basicData = soup.find(id="equipment-section")
    keys = basicData.find_all("dt")
    values = basicData.find_all("dd")
    newValues = [""] * len(values)
    tempDict = {}
    
    for index in range(len(values)):
        lis = values[index].find_all("li")
        for li in lis:
            if li != lis[len(lis)-1]:
                newValues[index] += li.get_text()+sep
            else:
                newValues[index] += li.get_text()

    for key, newValue in zip(keys, newValues):
        tempDict[key.get_text()] = newValue.replace("\u202f", " ")

    return tempDict

def createAdDict(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    ad = {"date": int(time.time()), "isPublished": False, "isSold": False}

    ad["model"] = soup.find(class_="StageTitle_makeModelContainer__RyjBP").get_text()
    ad["description"] = soup.find(class_="StageTitle_modelVersion__Yof2Z").get_text()
    ad["price"] = tools.formatPrice(soup.find(class_="PriceInfo_price__XU0aF").get_text())

    stats = soup.find_all(class_="VehicleOverview_itemText__AI4dA")
    ad["url"] = url
    ad["km"] = tools.formatKm(stats[0].get_text())
    ad["fuel"] = stats[3].get_text()
    ad["kw"], ad["ch"] = tools.formatPower(stats[4].get_text())
    release = stats[2].get_text()
    ad["release"] = tools.formatDate(release)
    transmissionOrAutonomy = stats[1].get_text()

    if "electrique" in ad["fuel"].lower():
        ad["fuel"] = ad["fuel"][1:]
        ad["autonomy"] = transmissionOrAutonomy
        ad["isAutomatic"] = True
    else:
        ad["isAutomatic"] = "automatique" in transmissionOrAutonomy.lower()

    ad["mainPicture"] = soup.find(class_="ImageWithBadge_picture__XJG24").find("img").get("src")
    
    carPassUrl = soup.find(class_="scr-link undefined")
    if carPassUrl:
        ad["carPassUrl"] = carPassUrl.get("href")

    dealerUrl = "/".join(soup.find(class_="scr-link DealerLinks_bold__urWLL").get("href").split("/")[:-1])
    ad["fk_dealer"] = models.Dealer.objects.get(url=dealerUrl)

    ad["basicData"] = json.dumps(getParsedHtmlTab(soup, "basic-details-section"))
    ad["history"] = json.dumps(getParsedHtmlTab(soup, "listing-history-section"))
    ad["technicalSpecs"] = json.dumps(getParsedHtmlTab(soup, "technical-details-section"))
    ad["consumption"] = json.dumps(getParsedHtmlTab(soup, "environment-details-section"))
    ad["appearance"] = json.dumps(getParsedHtmlTab(soup, "color-section"))
    ad["equipment"] = json.dumps(setEquipment(soup, "-----"))

    try:
        ad["summary"] = soup.find(class_="SellerNotesSection_content__te2EB").prettify()
    except:
        ad["summary"] = None

    # ajout des images

    pictures = soup.find_all(class_="image-gallery-thumbnail-image")[:1]
    ad["pictures"] = "-----".join([picture.get("src").replace("120x90.jpg", "1920x1080.webp") for picture in pictures])

  
    # suppression des clés sans valeurs
    for key in list(ad):
        if ad[key] == "-":
            del ad[key]

    return ad

def createAd(url):
    adDict = createAdDict(url)
    models.Ad.objects.create(**adDict)

def getDealerRemoteAdsUrls(dealer):
    url = models.Dealer.objects.get(name=dealer).url
    baseUrl = url

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    nbPages = len(soup.find_all(class_="pagination-item"))
    ads = soup.find_all(class_="dp-link dp-listing-item-title-wrapper")

    if nbPages > 1:

        for index in range(1, nbPages):
            url = baseUrl + "?page={}".format(index+1)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            ads += soup.find_all(class_="dp-link dp-listing-item-title-wrapper")

    adsUrls = []
    for ad in ads:
        adsUrls.append("https://autoscout24.be"+ad.get("href"))
    
    return adsUrls

def getAdsChanges(dealer):
    localAds = getDealerLocalAds(dealer)
    remoteAdsUrls = getDealerRemoteAdsUrls(dealer)

    # RENVOIT DES VOITURES EN DB LOCAL VENDUES
    adsSold = []
    for localAd in localAds:
        if localAd.url not in remoteAdsUrls:
            adsSold.append(localAd)
            localAds.delete()

    # AJOUT DES VOITURES EN DB LOCAL
    adsToAdd = []
    localAdsUrls = [ad.url for ad in localAds]
    for remoteAdUrl in remoteAdsUrls:
        if remoteAdUrl not in localAdsUrls:
            adsToAdd.append(remoteAdUrl)

    # MODIFICATION DES VOITURES EXISTANTES
    adsToEdit = []
    for localAd in localAds:
        oldAdDict = objToDict(localAd)
        newAdDict = createAdDict(localAd.url)


        keys = ["url", "price", "model", "basicData", "history", "technicalSpecs", "consumption", "appearance", "equipment", "summary", "description", "km", "fuel", "isAutomatic", "release", "kw", "ch", "mainPicture", "carPassUrl"]

        oldAdHash = dictToHash(oldAdDict, keys)
        newAdHash = dictToHash(newAdDict, keys)

        if oldAdHash != newAdHash:  
            adsToEdit.append({"oldAd": localAd, "newAd": newAdDict})

    return adsSold, adsToAdd, adsToEdit
            
def removeFormatOfSummary(summarySoup):
    lines = summarySoup.split("<br/>\r\n <br/>")
    newLines = []
    for line in lines:
        newLine = BeautifulSoup(line, "html.parser").get_text().replace("\n", "").replace("  ", "")
        newLines.append(newLine)
    summary = "\n".join(newLines)


    return summary

def uploadPicture(pictureUrl, dealer):
    url = f"{BASEURL}/{dealer.fbId}/photos"
    body = {"access_token": dealer.token, "published": False, "url": pictureUrl}

    response = requests.post(url, json=body)

    pictureId = response.json()["id"]
    return pictureId

def uploadPictureFromLocal(path, msg, dealer):
    url = f"{BASEURL}/{dealer.fbId}/photos"
    body = {"access_token": dealer.token, "message": msg}

    with open(path, "rb") as f:
        files = {"file": f}
    
        response = requests.post(url, data=body, files=files)


    pictureId = response.json()["id"]
    return pictureId

def uploadPictures(ad, dealer):
    pictures = ad.pictures.split("-----")

    picturesIds = []

    for picture in pictures:
        pictureId = uploadPicture(picture, dealer)
        picturesIds.append(pictureId)

    return picturesIds

def createPost(ad, msg, dealer):
    url = f"{BASEURL}/{dealer.fbId}/feed"
    body = {"message": msg, "access_token": dealer.token, "attached_media": []}

    picturesIds = uploadPictures(ad, dealer)

    for pictureId in picturesIds:
        body["attached_media"].append({"media_fbid": pictureId})

    ad.save()
    response = requests.post(url, json=body)
    if (response.status_code == 200):
        ad.isPublished = True
        ad.save()


def createRecap(msg, dealer):
    url = f"{BASEURL}/{dealer.fbId}/feed"
    body = {"message": msg, "access_token": dealer.token}

    response = requests.post(url, json=body)


def postNewAds(dealer):
    ads = models.Ad.objects.filter(isPublished=False, fk_dealer=dealer)
    for ad in ads:
        msg = f"""❗❗❗{boldText("NOUVEL ARRIVAGE")} ❗❗❗\n\nTrès beau modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        createPost(ad, msg, dealer)

def reuploadAds(weeks, dealer):
    ads = models.Ad.objects.filter(isPublished=True, fk_dealer=dealer)
    for ad in ads:
        if isTimestampOlderThan(weeks, ad.date):
            msg = f"""🚨🚨🚨{boldText("TOUJOURS DISPONIBLE")} 🚨🚨🚨\n\nCe modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")} est toujours disponible\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            createPost(ad, msg, dealer)
            ad.date = int(time.time())
            ad.save()

def postAdsRecap(weeks, dealer):
    ads = models.Ad.objects.filter(isPublished=True, fk_dealer=dealer)

    if len(ads) > 0:

        if isTimestampOlderThan(weeks ,ads[0].fk_dealer.fk_settings.lastSummary):
            lines = []
            for ad in ads:
                line = f"""{boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Pour + d'infos")} : {ad.url}\n{"-"*50}\n"""
                lines.append(line)

            lines.append(f"""\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}""")
            lines.append(f"""\n{boldText("Stock complet")} : {ad.fk_dealer.url}""")
            lines = "\n".join(lines)
            msg = f"🚨🚨🚨{boldText('Recapitulatif de nos modeles en stock')}🚨🚨🚨\n\n{lines}"
            createRecap(msg, dealer)

            ads[0].fk_dealer.fk_settings.lastSummary = int(time.time())
            ads[0].fk_dealer.fk_settings.save()


def postSoldAds(dealer):
    ads = models.Ad.objects.filter(isSold=True, fk_dealer=dealer)
    for ad in ads:
        createSoldPicture(ad)
        msg = f"""🚗🚗🚗{boldText("VEHICULE VENDU")}🚗🚗🚗\n\nFélicitation à l'acheteur de ce modèle {ad.model} pour son acquisition !\n\nVous pouvez retrouver l'ensemble de notre stock sur {ad.fk_dealer.url}"""
        uploadPictureFromLocal("media/modifiedFile.jpg", msg, dealer)
        ad.delete()

def postEditedAds(dealer):
    ads = models.Ad.objects.filter(isModified=True, fk_dealer=dealer)
    for ad in ads:
        msg = f"""❗❗❗{boldText("MODIFICATION D'ANNONCE")} ❗❗❗\n\nDes modifications ont été apportées à la fiche technique de ce modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        createPost(ad, msg, dealer)
        ad.isModified = False
        ad.save()

def postDiscountAds(dealer):
    ads = models.Ad.objects.filter(isModified=True, fk_dealer=dealer)
    for ad in ads:
        if ad.price < ad.lastPrice:
            msg = f"""💲💲💲{boldText("PROMOTION EXCEPTIONNELLE")} 💲💲💲\n\nLe prix de ce modèle de {boldText(ad.model)} est maintenant à {boldText(formatNumber(ad.price)+" €")} au lieu de {boldText(formatNumber(ad.lastPrice)+" €")} \n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            createPost(ad, msg, dealer)
            ad.isModified = False
            ad.save()

def createTestPost(dealer, scenario):

        if scenario == 0:
            ad = models.Ad.objects.filter(fk_dealer=dealer)[0]
            msg = f"""❗❗❗{boldText("NOUVEL ARRIVAGE")} ❗❗❗\n\nTrès beau modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            createPost(ad, msg, dealer)
        
        elif scenario == 1:
            ad = models.Ad.objects.filter(fk_dealer=dealer)[0]
            createSoldPicture(ad)
            msg = f"""🚗🚗🚗{boldText("VEHICULE VENDU")}🚗🚗🚗\n\nFélicitation à l'acheteur de ce modèle {ad.model} pour son acquisition !\n\nVous pouvez retrouver l'ensemble de notre stock sur {ad.fk_dealer.url}"""
            uploadPictureFromLocal("media/modifiedFile.jpg", msg, dealer)
        
        elif scenario == 2:
            ad = models.Ad.objects.filter(fk_dealer=dealer)[0]
            msg = f"""🚨🚨🚨{boldText("TOUJOURS DISPONIBLE")} 🚨🚨🚨\n\nCe modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")} est toujours disponible\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            createPost(ad, msg, dealer)

        elif scenario == 3:
            ad = models.Ad.objects.filter(fk_dealer=dealer)[0]
            msg = f"""💲💲💲{boldText("PROMOTION EXCEPTIONNELLE")} 💲💲💲\n\nLe prix de ce modèle de {boldText(ad.model)} est maintenant à {boldText(formatNumber(ad.price-2000)+" €")} au lieu de {boldText(formatNumber(ad.price)+" €")} \n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            createPost(ad, msg, dealer)

        elif scenario == 4:
            ad = models.Ad.objects.filter(fk_dealer=dealer)[0]
            msg = f"""❗❗❗{boldText("MODIFICATION D'ANNONCE")} ❗❗❗\n\nDes modifications ont été apportées à la fiche technique de ce modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            createPost(ad, msg, dealer)

        elif scenario == 5:
            ads = models.Ad.objects.filter(fk_dealer=dealer)
            lines = []
            for ad in ads:
                line = f"""{boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Pour + d'infos")} : {ad.url}\n{"-"*50}\n"""
                lines.append(line)
            lines.append(f"""\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}""")
            lines.append(f"""\n{boldText("Stock complet")} : {ad.fk_dealer.url}""")
            lines = "\n".join(lines)
            msg = f"🚨🚨🚨{boldText('Recapitulatif de nos modeles en stock')}🚨🚨🚨\n\n{lines}"
            createRecap(msg, dealer)

def scheduledTask():
    dealers = models.Dealer.objects.all()
    for dealer in dealers:
        adsSold, adsToAdd, adsToEdit = getAdsChanges(dealer.name)
        for ad in adsSold:
            ad.isSold = True
            ad.save()
        for ad in adsToAdd:
            createAd(ad)
        for ads in adsToEdit:
            ads["newAd"]["isModified"] = True
            ad = models.Ad.objects.get(id=ads["oldAd"].id)
            ad.lastPrice = ad.price
            ad.save()
            models.Ad.objects.filter(id=ads["oldAd"].id).update(**ads["newAd"])

        if dealer.fk_settings.createDiscountCarPost:
            postDiscountAds(dealer)
        if dealer.fk_settings.createModifiedPost:
            postEditedAds(dealer)

        if dealer.fk_settings.createNewCarPost:
            postNewAds(dealer)
        if dealer.fk_settings.createSoldCarPost:
            postSoldAds(dealer)
        if dealer.fk_settings.createOldCarPost:
            reuploadAds(dealer.fk_settings.oldCarPostDelay, dealer)
        if dealer.fk_settings.createSummaryPost:
            postAdsRecap(dealer.fk_settings.summaryPostDelay, dealer) 

