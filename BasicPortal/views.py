from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from BasicPortal.models import User, Car, Contract
from BasicPortal.serializers import UserSerializer

class GetUsers(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        users= User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response({serializer.data},status=status.HTTP_200_OK)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            token = Token.objects.get_or_create(user=serializer.validated_data['user'])
            return Response({serializer.data,token},status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        token = Token.objects.get(user=request.user)
        if token:
            token.delete()
            return Response(data=({'Message':'Logged out with grace'}),status=status.HTTP_200_OK)
        return Response(data=({'Error':'The Token does not exist'}),status=status.HTTP_400_BAD_REQUEST)
