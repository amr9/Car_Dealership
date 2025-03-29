from rest_framework import serializers
from BasicPortal.models import User, Car, Contract


class UserSerializer(serializers.Serializer):
    class Meta:
        model = User
        fields = '__all__'


class CarSerializer(serializers.Serializer):
    class Meta:
        model = Car
        fields = '__all__'

class ContractTypeSerializer(serializers.Serializer):
    class Meta:
        model = Contract
        fields = '__all__'
