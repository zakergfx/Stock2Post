import requests, time, json, os, hashlib, cv2, random
from datetime import datetime, timedelta
from PIL import Image, ImageDraw, ImageFont
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from . import models, tools, ig
import numpy as np

BASEURL = f"https://graph.facebook.com/v22.0"

def testing():
    pass

def createInstagramCover(ad):
    img = create_slide(ad, ad.mainPicture, 1080, 1920)
    cv2.imwrite("media/cover.jpg", img)
    return "https://stock2post.be/api/media/cover.jpg"

def init(dealer):
    adsSold, adsToAdd, adsToEdit = getAdsChanges(dealer.name, editedAds=False)
    for ad in adsToAdd:
        adDict = createAdDict(ad)
        adDict["isPublished"] = True
        models.Ad.objects.create(**adDict)
  
def cleanFbPage():
    dealers = models.Dealer.objects.all()
    for dealer in dealers:
        url = f"{BASEURL}/{dealer.fbId}/feed"
        headers = {"Authorization": f"OAuth {dealer.fbToken}"}
        response = requests.get(url, headers=headers).json()

        for line in response:
            url = f"{BASEURL}/{dealer.fbId}_{line['id'].split('_')[1]}"
            response = requests.delete(url, headers=headers)

        print("suppression ok")

def download_image(url):
    """Télécharge une image à partir d'une URL et renvoie l'image sous forme de tableau NumPy."""
    response = requests.get(url)
    if response.status_code == 200:
        # Convertir les données de l'image en un tableau NumPy
        img_array = np.frombuffer(response.content, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_COLOR)
        return img
    else:
        print(f"Erreur lors du téléchargement de l'image : {url}")
        return None

def putStats(rect_top, largeur, textes, draw):
    """
    Ajoute des statistiques sur l'image en utilisant l'objet draw.
    Cette fonction modifie directement l'objet draw qui affecte img_pil.
    """
    font_path = "arial.ttf"  # Changez ceci si nécessaire
    try:
        font = ImageFont.truetype(font_path, 40)
    except IOError:
        print(f"Impossible d'ouvrir la police '{font_path}'. Utilisation de la police par défaut.")
        font = ImageFont.load_default()

    # Utiliser l'objet draw passé en paramètre pour dessiner
    texte_couleur = (0, 0, 0)  # Noir

    # Dessiner les trois premiers textes à gauche
    for i, texte in enumerate(textes[:3]):
        text_bbox = draw.textbbox((0, 0), texte, font=font)
        text_width = text_bbox[2] - text_bbox[0]  # largeur
        text_height = text_bbox[3] - text_bbox[1]  # hauteur
        x = 100
        y = 250 + rect_top + text_height + 100 * i
        draw.text((x, y), texte, fill=texte_couleur, font=font)

    # Dessiner les trois derniers textes à droite
    for i, texte in enumerate(textes[3:]):
        text_bbox = draw.textbbox((0, 0), texte, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        x = largeur - text_width - 100
        y = 250 + rect_top + text_height + 100 * i
        draw.text((x, y), texte, fill=texte_couleur, font=font)

    # Pas besoin de retourner quoi que ce soit car draw modifie directement img_pil

def createVideo(ad):
    sortie = "media/diaporama0.mov"
    fps = 30  # Augmenter les FPS pour des transitions plus fluides
    duree_par_image = 3
    duree_transition = 1  # Durée de la transition en secondes

    hauteur, largeur = 1920, 1080
    taille = (largeur, hauteur)

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(sortie, fourcc, fps, taille)

    images_url = ad.pictures.split("-----")
    if len(images_url) > 10:
        images_url = images_url[:10]

    # Préparer toutes les images finales en avance
    final_images = []
    
    for image_url in images_url:
        final_image = create_slide(ad, image_url, hauteur, largeur)
        final_images.append(final_image)
    
    # Ajouter les images à la vidéo avec transitions
    for i in range(len(final_images)):
        current_image = final_images[i]
        
        # Ajouter l'image actuelle pendant la durée spécifiée (sans transition)
        frames_to_show = int(fps * (duree_par_image - duree_transition))
        for _ in range(frames_to_show):
            video.write(current_image)
        
        # Ajouter la transition vers la prochaine image
        if i < len(final_images) - 1:  # S'il y a une image suivante
            next_image = final_images[(i + 1)]
            transition_frames = int(fps * duree_transition)
            
            for j in range(transition_frames):
                # Calculer le facteur de mélange (0.0 à 1.0)
                alpha = j / transition_frames
                
                # Mélanger les deux images
                blended = cv2.addWeighted(current_image, 1 - alpha, next_image, alpha, 0)
                video.write(blended)

    video.release()

    print(f"Diaporama créé avec succès : {sortie}")
    if os.path.exists("media/diaporama.mov"):  # Vérifie si le fichier existe
        os.remove("media/diaporama.mov")
    os.system(f"ffmpeg -i {sortie} -c:v libx264 -b:v 5M -maxrate 25M -bufsize 10M -preset slow -c:a aac -b:a 128k media/diaporama.mov")
    print("Conversion encodage fini !")

def create_slide(ad, image_url, hauteur, largeur):
    """Crée une diapositive complète avec l'image et tous les textes"""
    img = download_image(image_url)
    
    # Calculer 45% de la hauteur totale pour l'image
    img_height = int(hauteur * 0.45)
    # Garder la largeur complète
    img_width = largeur
    
    # Redimensionner l'image en conservant les proportions
    img_aspect = img.shape[1] / img.shape[0]
    
    # Calculer les dimensions finales de l'image
    if img_aspect > (img_width / img_height):  # Image plus large que notre ratio
        new_width = img_width
        new_height = int(new_width / img_aspect)
    else:  # Image plus haute que notre ratio
        new_height = img_height
        new_width = int(new_height * img_aspect)
        
    # Redimensionner l'image
    img = cv2.resize(img, (new_width, new_height))

    # Créer un fond noir
    overlay = np.zeros((hauteur, largeur, 3), dtype=np.uint8)

    # Calculer la position pour centrer l'image horizontalement
    # et la placer en haut
    x_offset = (largeur - new_width) // 2
    y_offset = 0

    # Superposer l'image sur le fond noir
    overlay[y_offset:y_offset + new_height, x_offset:x_offset + new_width] = img

    # Le rectangle blanc commence juste après l'image (à 45% de la hauteur)
    rect_top = int(hauteur * 0.45)
    rect_bottom = hauteur
    rect_color = (255, 255, 255)
    cv2.rectangle(overlay, (0, rect_top), (largeur, rect_bottom), rect_color, -1)

    # Ajouter un rectangle gris en bas
    rect2_top = int(hauteur * 7.5 / 10)
    rect2_bottom = hauteur - 300
    rect2_color = (225, 225, 225)
    cv2.rectangle(overlay, (100, rect2_top), (largeur - 100, rect2_bottom), rect2_color, -1)

    # Convertir overlay en format PIL pour dessiner du texte
    img_pil = Image.fromarray(cv2.cvtColor(overlay, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(img_pil)

    # Ajouter le titre
    texte = ad.model
    font_path = "arial.ttf"
    try:
        font = ImageFont.truetype(font_path, 70)
    except IOError:
        print(f"Impossible d'ouvrir la police '{font_path}'. Utilisation de la police par défaut.")
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), texte, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = 100
    y = rect_top + text_height + 25
    draw.text((x, y), texte, fill=(0, 0, 0), font=font)

    # Ajouter le surtitre
    texte = "- NOUVEL ARRIVAGE -"
    font_path = "arialbd.ttf"
    try:
        font = ImageFont.truetype(font_path, 40)
    except IOError:
        print(f"Impossible d'ouvrir la police '{font_path}'. Utilisation de la police par défaut.")
        font = ImageFont.load_default()

    text_bbox = draw.textbbox((0, 0), texte, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (largeur - text_width) // 2
    y = rect_top + 20
    draw.text((x, y), texte, fill=(100, 100, 100), font=font)

    # Ajouter description
    font_path = "arial.ttf"
    try:
        font = ImageFont.truetype(font_path, 32)
    except IOError:
        print(f"Impossible d'ouvrir la police '{font_path}'. Utilisation de la police par défaut.")
        font = ImageFont.load_default()

    description = ad.description
    if len(description) > 35:
        description = description[:45] + "..."
    text_bbox = draw.textbbox((0, 0), description, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = 100
    y = rect_top + text_height + 150
    draw.text((x, y), description, fill=(100, 100, 100), font=font)

    # Ajouter le prix
    font_path = "arialbd.ttf"
    try:
        font = ImageFont.truetype(font_path, 70)
    except IOError:
        print(f"Impossible d'ouvrir la police '{font_path}'. Utilisation de la police par défaut.")
        font = ImageFont.load_default()

    price = f"{formatNumber(ad.price)} €"
    text_bbox = draw.textbbox((0, 0), price, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (largeur - text_width) // 2
    y = rect2_top + (rect2_bottom - rect2_top - text_height) // 2 - 10
    draw.text((x, y), price, fill=(0, 0, 0), font=font)

    # Ajouter contact
    font_path = "arialbd.ttf"
    try:
        font = ImageFont.truetype(font_path, 40)
    except IOError:
        print(f"Impossible d'ouvrir la police '{font_path}'. Utilisation de la police par défaut.")
        font = ImageFont.load_default()

    contact = f"{ad.fk_dealer.phone} - {ad.fk_dealer.mail}"
    text_bbox = draw.textbbox((0, 0), contact , font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (largeur - text_width) // 2
    y = rect_bottom - text_height - 150
    draw.text((x, y), contact , fill=(5, 0, 70), font=font)

    # Ajouter nom entreprise
    font_path = "arialbd.ttf"
    try:
        font = ImageFont.truetype(font_path, 40)
    except IOError:
        print(f"Impossible d'ouvrir la police '{font_path}'. Utilisation de la police par défaut.")
        font = ImageFont.load_default()

    company = f"- {ad.fk_dealer.name.upper()} -"
    text_bbox = draw.textbbox((0, 0), company, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    x = (largeur - text_width) // 2
    y = rect_bottom - text_height - 50
    draw.text((x, y), company, fill=(100, 100, 100), font=font)

    # Ajouter les statistiques
    # stats = ["Essence", "09/2020", "116 cv", "Boite automatique", "45 000 km", "Garantie 12 mois"]
    stats = [ad.fuel, ad.release, f'{ad.kw} kw ({ad.ch} ch)', "Automatique" if ad.isAutomatic else "Manuel" , f"{formatNumber(ad.km)} km", "Garantie 12 mois"]
    putStats(rect_top, largeur, stats, draw)

    # Convertir l'image PIL en tableau numpy pour OpenCV
    final_image = cv2.cvtColor(np.array(img_pil), cv2.COLOR_RGB2BGR)
    
    return final_image

def addImageToImage(imagePath, overlayPath, outputPath, littleness=2, position = None):
    # Ouvre les images
    baseImage = Image.open(imagePath).convert("RGBA")
    overlayImage = Image.open(overlayPath,).convert("RGBA")
    
    # Calcule le ratio pour redimensionner l'image de superposition sans la déformer
    overlayRatio = min(baseImage.width / overlayImage.width, baseImage.height / overlayImage.height)
    newSize = (int(1.5*overlayImage.width * overlayRatio)//littleness, int(1.5*overlayImage.height * overlayRatio)//littleness)
    overlayImage = overlayImage.resize(newSize, Image.LANCZOS)
    
    # Définit la position par défaut (centrée si non spécifiée)
    if position is None:
        position = ((baseImage.width - overlayImage.width) // 2, 
                    (baseImage.height - overlayImage.height) // 2)
    elif position == "up":
        position = ((baseImage.width - overlayImage.width) // 2, 
                    100)
    
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

def createDiscountPicture(ad):
    data = requests.get(ad.mainPicture).content
    with open ("media/originalFile.jpg", "wb") as f:
        f.write(data)

    addImageToImage("media/originalFile.jpg","media/discount.png", "media/modifiedFile.jpg", 2, "up")


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
    ad = {"date": int(time.time())+random.randint(0, 7200), "isPublished": False, "isSold": False}

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

    ads = []
    pagesRemaining = True

    index = 1
    while pagesRemaining:
        url = baseUrl + "?page={}".format(index)
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        pageAds = soup.find_all(class_="dp-link dp-listing-item-title-wrapper")
        index+=1
        if len(pageAds) > 0:
            ads += pageAds
        else:
            pagesRemaining= False

    adsUrls = []
    for ad in ads:
        adsUrls.append("https://autoscout24.be"+ad.get("href"))
    
    print("urls remote : "+str(len(adsUrls)))
    return adsUrls

def getAdsChanges(dealer, editedAds):
    localAds = getDealerLocalAds(dealer)
    remoteAdsUrls = getDealerRemoteAdsUrls(dealer)

    content = []
    with open(f"logs/logs-{int(time.time())}.txt", "w") as f:
        for localAd in localAds:
            content.append(localAd.url)

        content.sort()
        remoteAdsUrls.sort()
        content = ["LOCAL ADS"] + content + ["\nREMOTE ADS"] + remoteAdsUrls
        f.write("\n".join(content))
    
    # RENVOIT DES VOITURES EN DB LOCAL VENDUES
    adsSold = []
    for localAd in localAds:
        if localAd.url.split("-")[-1] not in [url.split("-")[-1] for url in remoteAdsUrls]:
            adsSold.append(localAd)
            # localAd.delete()

    # AJOUT DES VOITURES EN DB LOCAL
    adsToAdd = []
    localAdsUrls = [ad.url for ad in localAds]
    for remoteAdUrl in remoteAdsUrls:
        if remoteAdUrl.split("-")[-1] not in [url.split("-")[-1] for url in localAdsUrls]:
            adsToAdd.append(remoteAdUrl)
    
    adsToEdit = []
    if editedAds:
        # MODIFICATION DES VOITURES EXISTANTES
        for localAd in localAds:
            oldAdDict = objToDict(localAd)

            if localAd not in adsSold:
                newAdDict = createAdDict(localAd.url)

                keys = ["price", "model", "basicData", "history", "technicalSpecs", "consumption", "appearance", "equipment", "summary", "description", "km", "fuel", "isAutomatic", "release", "kw", "ch", "mainPicture", "carPassUrl"]

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
    body = {"access_token": dealer.fbToken, "published": False, "url": pictureUrl}

    response = requests.post(url, json=body)

    print("picture", response.json())
    pictureId = response.json()["id"]
    return pictureId

def uploadPictureFromLocal(path, msg, dealer):
    url = f"{BASEURL}/{dealer.fbId}/photos"
    body = {"access_token": dealer.fbToken, "message": msg}

    with open(path, "rb") as f:
        files = {"file": f}
    
        response = requests.post(url, data=body, files=files)


    print("avant pictureId", response.json())
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
    print("Creating new car post")
    url = f"{BASEURL}/{dealer.fbId}/feed"
    body = {"message": msg, "access_token": dealer.fbToken, "attached_media": []}

    picturesIds = uploadPictures(ad, dealer)

    for pictureId in picturesIds:
        body["attached_media"].append({"media_fbid": pictureId})

    ad.save()
    response = requests.post(url, json=body)



def createRecap(msg, dealer):
    url = f"{BASEURL}/{dealer.fbId}/feed"
    body = {"message": msg, "access_token": dealer.fbToken}

    response = requests.post(url, json=body)


def postNewAds(dealer):
    ads = models.Ad.objects.filter(isPublished=False, fk_dealer=dealer)
    for ad in ads:
        if ad.date > dealer.fk_settings.lastNewCarPostEnabled:
            msg = f"""❗❗❗{boldText("NOUVEL ARRIVAGE")} ❗❗❗\n\nTrès beau modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""

            if dealer.fbToken:
                createPost(ad, msg, dealer)

            if dealer.igToken:
                imageUrls = ad.pictures.split("-----")
                print("0")
                mediaId = ig.createCarouselContainer(dealer, imageUrls, msg)
                print("1")
                ig.publishMedia(dealer, mediaId)
                print("2")

            if dealer.fk_settings.createNewCarStory:
                if dealer.fbToken:
                    postNewAdStory(dealer, ad)
                if dealer.igToken:
                    videoUrl = "https://stock2post.be/api/media/diaporama.mov"
                    message = f"""❗❗❗{boldText("NOUVEL ARRIVAGE")} ❗❗❗\n\nTrès beau modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
                    mediaId = ig.createVideoContainer(dealer, videoUrl, message, "STORIES")
                    ig.publishMedia(dealer, mediaId)
                    # mediaId = ig.createVideoContainer(dealer, videoUrl, message, "REELS")
                    # ig.publishMedia(dealer, mediaId)

            ad.isPublished = True
            ad.save()

def postNewAdsStory(dealer):
    ads = models.Ad.objects.filter(isPublished=False, fk_dealer=dealer)
    for ad in ads:
        if ad.date > dealer.fk_settings.lastNewCarPostEnabled:
            if dealer.fbToken:
                postNewAdStory(dealer, ad)
            if dealer.igToken:
                videoUrl = "https://stock2post.be/api/media/diaporama.mov"
                message = f"""❗❗❗{boldText("NOUVEL ARRIVAGE")} ❗❗❗\n\nTrès beau modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
                mediaId = ig.createVideoContainer(dealer, videoUrl, message, "STORIES")
                ig.publishMedia(dealer, mediaId)
                # mediaId = ig.createVideoContainer(dealer, videoUrl, message, "REELS")
                # ig.publishMedia(dealer, mediaId)

            ad.isPublished = True
            ad.save()

def postNewAdStory(dealer, ad):
    print("Creating new car story")
    createVideo(ad)
    publishVideo(dealer)


def publishVideo(dealer):
    # start upload session
    url = f"https://graph.facebook.com/v22.0/{dealer.fbId}/video_stories"
    headers = {"Authorization": f"OAuth {dealer.fbToken}"}
    body = {"upload_phase": "start"}

    response = requests.post(url=url, json=body, headers=headers)
    videoId = response.json()["video_id"]

    # upload the video
    url = f"https://rupload.facebook.com/video-upload/v22.0/{videoId}"
    videoPath = "media/diaporama.mov"
    headers = {"Authorization": f"OAuth {dealer.fbToken}", "offset": "0", "file_size": str(os.path.getsize(videoPath)), "Content-Type": "video/quicktime"}

    with open(videoPath, "rb") as f:
        response = requests.post(url=url, json=body, headers=headers, data=f)
        response = response.json()

    # publish as story
    url = f"https://graph.facebook.com/v22.0/{dealer.fbId}/video_stories"
    headers = {"Authorization": f"OAuth {dealer.fbToken}"}
    body = {"video_id": videoId, "upload_phase": "finish"}

    response = requests.post(url=url, json=body, headers=headers)

    if response.status_code == 200:
        print("upload story success")


def reuploadAds(weeks, dealer):
    ads = models.Ad.objects.filter(isPublished=True, fk_dealer=dealer)
    for ad in ads:
        if isTimestampOlderThan(weeks, ad.date):
            msg = f"""🚨🚨🚨{boldText("TOUJOURS DISPONIBLE")} 🚨🚨🚨\n\nCe modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")} est toujours disponible\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        
            if dealer.fbToken:
                createPost(ad, msg, dealer)

            if dealer.igToken:
                imageUrls = ad.pictures.split("-----")
                mediaId = ig.createCarouselContainer(dealer, imageUrls, msg)
                ig.publishMedia(dealer, mediaId)

            ad.date = int(time.time())
            ad.save()

def postAdsRecap(weeks, dealer):
    ads = models.Ad.objects.filter(isPublished=True, fk_dealer=dealer)

    if len(ads) > 0 and dealer.fbToken:

        if isTimestampOlderThan(weeks ,ads[0].fk_dealer.fk_settings.lastSummary):
            lines = []
            for ad in ads:
                line = f"""{boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Pour + d'infos")} : {ad.url}\n{"-"*50}\n"""
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
        
        if dealer.fbToken:
            uploadPictureFromLocal("media/modifiedFile.jpg", msg, dealer)

        if dealer.igToken:
            # impossible de faire ca avec une adresse local
            imageUrl = f'https://stock2post.be/api/media/modifiedFile.jpg'
            mediaId = ig.createImageContainer(dealer, imageUrl, msg)
            ig.publishMedia(dealer, mediaId)

        ad.delete()

def postEditedAds(dealer):
    ads = models.Ad.objects.filter(isModified=True, fk_dealer=dealer)
    for ad in ads:
        msg = f"""❗❗❗{boldText("MODIFICATION D'ANNONCE")} ❗❗❗\n\nDes modifications ont été apportées à la fiche technique de ce modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        
        if dealer.fbToken:
            createPost(ad, msg, dealer)

        if dealer.igToken:
            imageUrls = ad.pictures.split("-----")
            mediaId = ig.createCarouselContainer(dealer, imageUrls, msg)
            ig.publishMedia(dealer, mediaId)

        ad.isModified = False
        ad.save()

def postDiscountAds(dealer):
    ads = models.Ad.objects.filter(isModified=True, fk_dealer=dealer)
    for ad in ads:
        if ad.price < ad.lastPrice:
            createDiscountPicture(ad)
            msg = f"""💲💲💲{boldText("PROMOTION EXCEPTIONNELLE")} 💲💲💲\n\nLe prix de ce modèle de {boldText(ad.model)} est maintenant à {boldText(formatNumber(ad.price)+" €")} au lieu de {boldText(formatNumber(ad.lastPrice)+" €")} \n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            if dealer.fbToken:
                uploadPictureFromLocal("media/modifiedFile.jpg", msg, dealer)

            if dealer.igToken:
                # impossible de faire ca avec une adresse local
                imageUrl = f'https://stock2post.be/api/media/modifiedFile.jpg'
                mediaId = ig.createImageContainer(dealer, imageUrl, msg)
                ig.publishMedia(dealer, mediaId)
            
            ad.isModified = False
            ad.save()

def deleteSoldAds(dealer):
    ads = models.Ad.objects.filter(fk_dealer=dealer, isSold=True)
    ads.delete()

def createTestPost(dealer, scenario):
    if scenario == 0:
        print("here scenario 0")
        ad = models.Ad.objects.filter(fk_dealer=dealer).last()
        msg = f"""❗❗❗{boldText("NOUVEL ARRIVAGE")} ❗❗❗\n\nTrès beau modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        
        if dealer.fbToken:
            createPost(ad, msg, dealer)

        if dealer.igToken:
            # coverUrl = createInstagramCover(ad)
            # imageUrls = [coverUrl]+ad.pictures.split("-----")
            imageUrls = ad.pictures.split("-----")
            mediaId = ig.createCarouselContainer(dealer, imageUrls, msg)
            ig.publishMedia(dealer, mediaId)
    
    elif scenario == 1:
        ad = models.Ad.objects.filter(fk_dealer=dealer).last()
        msg = f"""🚗🚗🚗{boldText("VEHICULE VENDU")}🚗🚗🚗\n\nFélicitation à l'acheteur de ce modèle {ad.model} pour son acquisition !\n\nVous pouvez retrouver l'ensemble de notre stock sur {ad.fk_dealer.url}"""
        
        if dealer.fbToken:
            uploadPictureFromLocal("media/modifiedFile.jpg", msg, dealer)

        if dealer.igToken:
            # impossible de faire ca avec une adresse local
            imageUrl = f'https://stock2post.be/api/media/modifiedFile.jpg'
            mediaId = ig.createImageContainer(dealer, imageUrl, msg)
            ig.publishMedia(dealer, mediaId)
    
    elif scenario == 2:
        ad = models.Ad.objects.filter(fk_dealer=dealer).last()
        msg = f"""🚨🚨🚨{boldText("TOUJOURS DISPONIBLE")} 🚨🚨🚨\n\nCe modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")} est toujours disponible\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        
        if dealer.fbToken:
            createPost(ad, msg, dealer)

        if dealer.igToken:
            imageUrls = ad.pictures.split("-----")
            mediaId = ig.createCarouselContainer(dealer, imageUrls, msg)
            ig.publishMedia(dealer, mediaId)

    elif scenario == 3:
        ad = models.Ad.objects.filter(fk_dealer=dealer).last()
        msg = f"""💲💲💲{boldText("PROMOTION EXCEPTIONNELLE")} 💲💲💲\n\nLe prix de ce modèle de {boldText(ad.model)} est maintenant à {boldText(formatNumber(ad.price-2000)+" €")} au lieu de {boldText(formatNumber(ad.price)+" €")} \n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        createDiscountPicture(ad)

        if dealer.fbToken:
            uploadPictureFromLocal("media/modifiedFile.jpg", msg, dealer)

        if dealer.igToken:
            # impossible de faire ca avec une adresse local
            imageUrl = f'https://stock2post.be/api/media/modifiedFile.jpg'
            mediaId = ig.createImageContainer(dealer, imageUrl, msg)
            ig.publishMedia(dealer, mediaId)

    elif scenario == 4:
        ad = models.Ad.objects.filter(fk_dealer=dealer).last()
        
        msg = f"""❗❗❗{boldText("MODIFICATION D'ANNONCE")} ❗❗❗\n\nDes modifications ont été apportées à la fiche technique de ce modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
        
        if dealer.fbToken:
            createPost(ad, msg, dealer)

        if dealer.igToken:
            imageUrls = ad.pictures.split("-----")
            mediaId = ig.createCarouselContainer(dealer, imageUrls, msg)
            ig.publishMedia(dealer, mediaId)

    elif scenario == 5:
        ads = models.Ad.objects.filter(fk_dealer=dealer)
        lines = []
        for ad in ads:
            line = f"""{boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Pour + d'infos")} : {ad.url}\n{"-"*50}\n"""
            lines.append(line)
        lines.append(f"""\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}""")
        lines.append(f"""\n{boldText("Stock complet")} : {ad.fk_dealer.url}""")
        lines = "\n".join(lines)
        msg = f"🚨🚨🚨{boldText('Recapitulatif de nos modeles en stock')}🚨🚨🚨\n\n{lines}"
        
        if dealer.fbToken:
            createRecap(msg, dealer)

    elif scenario == 6:
        ad = models.Ad.objects.filter(fk_dealer=dealer).last()
        createVideo(ad)

        if dealer.fbToken:
            publishVideo(ad.fk_dealer)

        if dealer.igToken:
            videoUrl = "https://stock2post.be/api/media/diaporama.mov"
            message = f"""❗❗❗{boldText("NOUVEL ARRIVAGE")} ❗❗❗\n\nTrès beau modèle de {boldText(ad.model)} au prix de {boldText(formatNumber(ad.price)+" €")}\n\n🛣️ {boldText("Premiere immatriculation")} : {ad.release}\n🌍 {boldText("Kilometrage")} : {formatNumber(ad.km)} km\n⛽ {boldText("Carburant")} : {ad.fuel}\n🛞 {boldText("Transmission")} : {"Automatique" if ad.isAutomatic else "Manuelle"}\n🚀 {boldText("Puissance")} : {ad.kw} kw ({ad.ch} ch)\n\n{boldText("Telephone")} : {ad.fk_dealer.phone}\n{boldText("Mail")} : {ad.fk_dealer.mail}\n\n{boldText("Pour + d'infos")} : {ad.url}"""
            
            mediaId = ig.createVideoContainer(dealer, videoUrl, message, "STORIES")
            ig.publishMedia(dealer, mediaId)

            # mediaId = ig.createVideoContainer(dealer, videoUrl, message, "REELS")
            # ig.publishMedia(dealer, mediaId)

    dealer.requestStatus = "success"
    dealer.save()


def scheduledTask():
    dealers = models.Dealer.objects.all()
    for dealer in dealers:
        if dealer.isInit:
            print("normal sched task "+dealer.name)
            adsSold, adsToAdd, adsToEdit = getAdsChanges(dealer.name, editedAds=dealer.fk_settings.createDiscountCarPost or dealer.fk_settings.createModifiedPost)
            print(f"ads to sold: {len(adsSold)}")
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


            if not dealer.fk_settings.pageIsPaused:
                if dealer.fk_settings.createNewCarPost:
                    postNewAds(dealer)
                if dealer.fk_settings.createNewCarStory:
                    postNewAdsStory(dealer)
                if dealer.fk_settings.createSoldCarPost:
                    postSoldAds(dealer)
                    deleteSoldAds(dealer)
                if dealer.fk_settings.createDiscountCarPost:
                    postDiscountAds(dealer)
                if dealer.fk_settings.createModifiedPost: # discount avant edited comme ca pas de doublon
                    postEditedAds(dealer)
                if dealer.fk_settings.createOldCarPost: # + 2h chaque fois pour eviter le spam
                    reuploadAds(dealer.fk_settings.oldCarPostDelay, dealer)
                if dealer.fk_settings.createSummaryPost:
                    postAdsRecap(dealer.fk_settings.summaryPostDelay, dealer) 
        else:
            print("init "+dealer.name)
            init(dealer)
            dealer.isInit = True
            dealer.save()

