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
from PIL import Image


TOKEN = "EAAIzZAhit7IcBOZBUWySlTzLE5AMPPEnjsCZBqEESOviSqO366xgOQDQTpf3cT7RWJfPEmn7ZARzdZBHjWBOu5bWTAh4D1UwDLFsWgZCLNT0Ee1EEvrVruZBuHZBupihuFTl5mzlSvCiwP65WnbgZCcQrmfbsGAKRBcZATeRmeru3zzVBgWHfbSIZBQuc5ZBGvdA0los"
PAGEID = "530119660189423"
BASEURL = f"https://graph.facebook.com/v22.0/{PAGEID}"

def testing():
    scheduledTask()
    # postAdsRecap()
    # postNewAds()

def cleanFbPage():
    url = f"{BASEURL}/feed"
    headers = {"Authorization": f"OAuth {TOKEN}"}
    response = requests.get(url, headers=headers).json()["data"]
    
    for line in response:
        url = f"{BASEURL}_{line['id'].split('_')[1]}"
        response = requests.delete(url, headers=headers)

    print("suppression ok")

def addImageToImage(imagePath, overlayPath, outputPath, position=None):
        # Ouvre les images
    baseImage = Image.open(imagePath).convert("RGBA")
    overlayImage = Image.open(overlayPath,).convert("RGBA")
    
    # Calcule le ratio pour redimensionner l'image de superposition sans la déformer
    overlayRatio = min(baseImage.width / overlayImage.width, baseImage.height / overlayImage.height)
    newSize = (int(overlayImage.width * overlayRatio)//2, int(overlayImage.height * overlayRatio)//2)
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

    dealerUrl = soup.find(class_="scr-link StockList_link__K_aw7").get("href")
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

    pictures = soup.find_all(class_="image-gallery-thumbnail-image")
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
    for ad in ads[:3]:
        adsUrls.append("https://autoscout24.be"+ad.get("href"))
    
    return adsUrls

def getAdsChanges(dealer):
    localAds = getDealerLocalAds(dealer)
    remoteAdsUrls = getDealerRemoteAdsUrls(dealer)

    # RENVOIT DES VOITURES EN DB LOCAL VENDUES
    adsSold = []
    for localAd in localAds:
        # if localAd.url not in remoteAdsUrls:
        adsSold.append(localAd)

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



    
        
def uploadPicture(pictureUrl):
    url = f"{BASEURL}/photos"
    body = {"access_token": TOKEN, "published": False, "url": pictureUrl}

    response = requests.post(url, json=body)


    pictureId = response.json()["id"]
    return pictureId

def uploadPictureFromLocal(path, msg):
    url = f"{BASEURL}/photos"
    body = {"access_token": TOKEN, "message": msg}

    with open(path, "rb") as f:
        files = {"file": f}
    
        response = requests.post(url, data=body, files=files)


    pictureId = response.json()["id"]
    return pictureId

def uploadPictures(ad):
    pictures = ad.pictures.split("-----")[:3]

    picturesIds = []

    for picture in pictures:
        pictureId = uploadPicture(picture)
        picturesIds.append(pictureId)

    return picturesIds

def createPost(ad, msg):
    url = f"{BASEURL}/feed"
    body = {"message": msg, "access_token": TOKEN, "attached_media": []}

    picturesIds = uploadPictures(ad)

    for pictureId in picturesIds:
        body["attached_media"].append({"media_fbid": pictureId})

    ad.save()
    response = requests.post(url, json=body)
    if (response.status_code == 200):
        ad.isPublished = True


def createRecap(msg):
    url = f"{BASEURL}/feed"
    body = {"message": msg, "access_token": TOKEN}

    response = requests.post(url, json=body)


def postNewAds():
    ads = models.Ad.objects.filter(isPublished=False)
    for ad in ads:
        msg = f"""❗❗❗{boldText("NOUVEL ARRIVAGE")} ❗❗❗\n\nTrès beau modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        createPost(ad, msg)

def reuploadAds(weeks):
    ads = models.Ad.objects.filter(isPublished=True)
    for ad in ads:
        if isTimestampOlderThan(weeks, ad.date):
            msg = f"""🚨🚨🚨{boldText("TOUJOURS DISPONIBLE")} 🚨🚨🚨\n\nCe modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")} est toujours disponible\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            createPost(ad, msg)

def postAdsRecap(weeks):
    ads = models.Ad.objects.filter(isPublished=True)

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
            createRecap(msg)

def postSoldAds():
    ads = models.Ad.objects.filter(isSold=True)
    for ad in ads:
        createSoldPicture(ad)
        msg = f"""🚗🚗🚗{boldText("VEHICULE VENDU")}🚗🚗🚗\n\nFélicitation à l'acheteur de ce modèle {ad.model} pour son acquisition !\n\nVous pouvez retrouver l'ensemble de notre stock sur {ad.fk_dealer.url}"""
        uploadPictureFromLocal("media/modifiedFile.jpg", msg)
        ad.delete()

def postEditedAds():
    ads = models.Ad.objects.filter(isModified=True)
    for ad in ads:
        msg = f"""❗❗❗{boldText("MODIFICATION D'ANNONCE")} ❗❗❗\n\nDes modifications ont été apportées à la fiche technique de ce modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        createPost(ad, msg)
        ad.isModified = False
        ad.save()

def postDiscountAds():
    ads = models.Ad.objects.filter(isModified=True)
    for ad in ads:
        if ad.price < ad.lastPrice:
            msg = f"""💲💲💲{boldText("PROMOTION EXCEPTIONNELLE")} 💲💲💲\n\nLe prix de ce modèle de {boldText(ad.model)} est maintenant à {boldText(formatNumber(ad.price)+" €")} au lieu de {boldText(formatNumber(ad.lastPrice)+" €")} \n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release.split("/")[0]}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            createPost(ad, msg)
            ad.isModified = False
            ad.save()

def scheduledTask():
    dealers = models.Dealer.objects.all()
    for dealer in dealers:
        adsSold, adsToAdd, adsToEdit = getAdsChanges(dealer.name)
        for ad in adsSold:
            ad.isSold = True
            ad.save()
        for ad in adsToAdd:
            createAd(ad)
        # for ads in adsToEdit:
        #     ads["newAd"]["isModified"] = True
        #     ad = models.Ad.objects.get(id=ads["oldAd"].id)
        #     ad.lastPrice = ad.price
        #     ad.save()
        #     models.Ad.objects.filter(id=ads["oldAd"].id).update(**ads["newAd"])

        # if dealer.fk_settings.createDiscountCarPost:
        #     postDiscountAds()
        # if dealer.fk_settings.createModifiedPost:
        #     postEditedAds()


        if dealer.fk_settings.createNewCarPost:
            postNewAds()
        if dealer.fk_settings.createSoldCarPost:
            postSoldAds()
        # if dealer.fk_settings.createOldCarPost:
        #     reuploadAds(dealer.fk_settings.oldCarPostDelay)
        # if dealer.fk_settings.createSummaryPost:
        #     postAdsRecap(dealer.fk_settings.summaryPostDelay) 

