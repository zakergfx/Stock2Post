import requests
from . import models

def IGcreateImageContainer(dealer, imageUrl, message):
    url = f"https://graph.instagram.com/v22.0/{dealer.igId}/media?access_token={dealer.igToken}"
    body = {"image_url": imageUrl, "caption": message}
    mediaId = requests.post(url, json=body).json()["id"]

    return mediaId

def IGcreateCarouselContainer(dealer, imageUrls, message):
    url = f"https://graph.instagram.com/v22.0/{dealer.igId}/media?access_token={dealer.igToken}"
    
    mediaIds = []
    for imageUrl in imageUrls:
        body = {"image_url": imageUrl, "is_carousel_item": True}
        mediaId = requests.post(url, json=body).json()["id"]
        mediaIds.append(mediaId)

    body = {"caption": message, "media_type": "CAROUSEL", "children": ",".join(mediaIds)}
    mediaId = requests.post(url, json=body).json()["id"]

    return mediaId

def IGPublishMedia(dealer, mediaId):
    url = f"https://graph.instagram.com/v22.0/{dealer.igId}/media_publish?access_token={dealer.igToken}"
    body = {"creation_id": mediaId}
    response = requests.post(url, json=body)