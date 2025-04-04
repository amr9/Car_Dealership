from rest_framework.authentication import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from BasicPortal.models import User, Car, Contract


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name', 'is_active','date_joined', 'last_login']

class CarSerializer(ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'


class ContractTypeSerializer(ModelSerializer):
    class Meta:
        model = Contract
        fields = '__all__'

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid credentials")
        data['user'] = user
        return data