from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from BasicPortal.models import User, Car, Contract
from BasicPortal.serializers import UserSerializer, LoginSerializer


class GetUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:

            users = User.objects.all()
            serializer = UserSerializer(users, many=True)
            return Response({'users': serializer.data}, status=status.HTTP_200_OK)

        except Exception as e:

            return Response(data={'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                "user": {
                    "id": user.id,
                    "username": user.username
                },
                "token": token.key
            })
        return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = Token.objects.get(user=request.user)
        if token:
            token.delete()
            return Response(data={"Message": "Logged out with grace"}, status=status.HTTP_200_OK)
        return Response(data={"Error": "The Token does not exist"}, status=status.HTTP_400_BAD_REQUEST)

class Register(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        return Response(data={"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)