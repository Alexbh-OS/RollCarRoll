from rest_framework import serializers

from storage.models import Dealer, Car




class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ['id','title','city','address','area','rating']


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['id','firm','model','year','power','color','price','dealer']

