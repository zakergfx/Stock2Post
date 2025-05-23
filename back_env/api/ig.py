import requests, time
from . import models

def createImageContainer(dealer, imageUrl, message):
    url = f"https://graph.instagram.com/v22.0/{dealer.igId}/media?access_token={dealer.igToken}"
    body = {"image_url": imageUrl, "caption": message}
    response = requests.post(url, json=body).json()

    return response["id"]

def createCarouselContainer(dealer, imageUrls, message):

    if len(imageUrls) > 10:
        imageUrls = imageUrls[:10]

    url = f"https://graph.instagram.com/v22.0/{dealer.igId}/media?access_token={dealer.igToken}"
    
    mediaIds = []
    for imageUrl in imageUrls:
        body = {"image_url": imageUrl, "is_carousel_item": True}
        response = requests.post(url, json=body).json()
        mediaIds.append(response["id"])

    body = {"caption": message, "media_type": "CAROUSEL", "children": ",".join(mediaIds)}
    response = requests.post(url, json=body).json()

    return response["id"]

def createVideoContainer(dealer, videoUrl, message, videoType):
    url = f"https://graph.instagram.com/v22.0/{dealer.igId}/media?access_token={dealer.igToken}"
    body = {"video_url": videoUrl, "media_type": videoType, "caption": message}
    response= requests.post(url, json=body).json()

    return response["id"]

def publishMedia(dealer, mediaId):
    url = f"https://graph.instagram.com/v22.0/{dealer.igId}/media_publish?access_token={dealer.igToken}"
    body = {"creation_id": mediaId}

    uploadOk = False

    cpt = 0
    while not uploadOk and cpt < 20:
        response = requests.post(url, json=body).json()
        print("publishMedia: ", response)
        if "id" in response:
            uploadOk = True
            print("upload ok")
        elif "error" in response:
            if response["error"]["message"] == "Application request limit reached":
                uploadOk = True
                print("upload ok (limit msg)")
            else:
                time.sleep(5)
        print(f"tentative: {cpt}")
        cpt += 1
    print("end")
