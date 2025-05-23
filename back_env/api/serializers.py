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

class MakeSerializer(ModelSerializer):
    class Meta:
        model = models.Make
        fields = '__all__'


class ModelSerializer(ModelSerializer):
    class Meta:
        model = models.Model
        fields = '__all__'

