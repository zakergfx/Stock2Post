from rest_framework.serializers import ModelSerializer
from . import models
        
class SettingsSerializer(ModelSerializer):
    class Meta:
        model = models.Settings
        fields = '__all__'

class DealerSerializer(ModelSerializer):
    fk_settings = SettingsSerializer()

    class Meta:
        model = models.Dealer
        fields = '__all__'

class AdSerializer(ModelSerializer):
    class Meta:
        model = models.Ad
        fields = '__all__'

