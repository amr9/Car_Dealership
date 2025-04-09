from rest_framework.authentication import authenticate
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from BasicPortal.models import User, Car, Contract


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name','last_name', 'is_active','date_joined', 'last_login']
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()
        return instance

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