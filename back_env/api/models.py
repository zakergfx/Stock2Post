from django.db import models
from django.conf import settings
import time


def get_current_timestamp():
    return int(time.time())

class Settings(models.Model):
    FBpageIsPaused = models.BooleanField(default=True)
    FBcreateNewCarPost = models.BooleanField(default=False)
    FBcreateNewCarStory = models.BooleanField(default=False)
    FBcreateSoldCarPost = models.BooleanField(default=False)
    FBcreateOldCarPost = models.BooleanField(default=False)
    FBcreateDiscountCarPost = models.BooleanField(default=False)
    FBoldCarPostDelay = models.PositiveIntegerField(default=4)
    FBlastNewCarPostEnabled = models.PositiveIntegerField(default=get_current_timestamp)

    IGpageIsPaused = models.BooleanField(default=True)
    IGcreateNewCarPost = models.BooleanField(default=False)
    IGcreateNewCarStory = models.BooleanField(default=False)
    IGcreateSoldCarPost = models.BooleanField(default=False)
    IGcreateOldCarPost = models.BooleanField(default=False)
    IGcreateDiscountCarPost = models.BooleanField(default=False)
    IGoldCarPostDelay = models.PositiveIntegerField(default=0)
    IGlastNewCarPostEnabled = models.PositiveIntegerField(default=get_current_timestamp)

class Dealer(models.Model):
    name = models.CharField(max_length=500)
    url = models.CharField(max_length=500)
    mail = models.CharField(max_length=500)
    phone = models.CharField(max_length=500)

    fbPageName = models.CharField(default=None, null=True, blank=True, max_length=500)
    fbId = models.PositiveIntegerField(default=None, blank=True, null=True)
    fbToken = models.CharField(max_length=500, null=True, blank=True)

    igPageName = models.CharField(default=None, null=True, blank=True, max_length=500)
    igId = models.PositiveIntegerField(default=None, blank=True, null=True)
    igToken = models.CharField(max_length=500, null=True, blank=True)

    isInit = models.BooleanField(default=False)

    requestStatus = models.CharField(max_length=500, default=None, null=True, blank=True)

    fk_settings = models.OneToOneField(Settings, on_delete=models.CASCADE)
    fk_user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name

class Ad(models.Model):
    url = models.CharField(max_length=500)
    price = models.PositiveIntegerField()
    lastPrice = models.PositiveIntegerField(null=True, blank=True)
    model = models.CharField(max_length=500)

    basicData = models.TextField()
    history = models.TextField()
    technicalSpecs = models.TextField()
    consumption = models.TextField()
    appearance = models.TextField()
    equipment = models.TextField()
    summary = models.TextField(null=True, blank=True)

    description = models.CharField(max_length=500)
    km = models.PositiveIntegerField()
    fuel = models.CharField(max_length=500)
    isAutomatic = models.BooleanField()
    autonomy = models.CharField(max_length=500, null=True, blank=True)
    release = models.CharField(max_length=500)
    kw = models.PositiveIntegerField()
    ch = models.PositiveIntegerField()
    mainPicture = models.CharField(max_length=500)
    pictures = models.CharField(max_length=50000, null=True,blank=True)
    carPassUrl = models.CharField(max_length=500, null=True, blank=True)
    date = models.PositiveBigIntegerField()
    isPublished = models.BooleanField()
    isSold = models.BooleanField()

    fk_dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)


class Make(models.Model):
    as_id = models.PositiveIntegerField()
    name = models.CharField(max_length=500)

    def __str__(self):
        return self.name


class Model(models.Model):
    as_id = models.PositiveIntegerField()
    name = models.CharField(max_length=500)
    vehicleType = models.CharField(max_length=1)
    fk_make = models.ForeignKey(Make, on_delete=models.CASCADE)