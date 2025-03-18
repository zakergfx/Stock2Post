from django.db import models
from django.conf import settings
import time


def get_current_timestamp():
    return int(time.time())

class Settings(models.Model):
    pageIsPaused = models.BooleanField(default=True)
    createNewCarPost = models.BooleanField(default=False)
    createNewCarStory = models.BooleanField(default=False)
    createSoldCarPost = models.BooleanField(default=False)
    createOldCarPost = models.BooleanField(default=False)
    createDiscountCarPost = models.BooleanField(default=False)
    createSummaryPost = models.BooleanField(default=False)
    createModifiedPost = models.BooleanField(default=False)

    oldCarPostDelay = models.PositiveIntegerField(default=4)
    summaryPostDelay = models.PositiveIntegerField(default=4)

    lastSummary = models.PositiveIntegerField(default=get_current_timestamp)
    lastNewCarPostEnabled = models.PositiveIntegerField(default=get_current_timestamp)

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
    pictures = models.CharField(max_length=50000)
    carPassUrl = models.CharField(max_length=500, null=True, blank=True)
    date = models.PositiveBigIntegerField()
    isPublished = models.BooleanField()
    isSold = models.BooleanField()
    isModified = models.BooleanField(default=False)

    fk_dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)


