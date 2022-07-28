from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from user.models import UsersModel
from user.serializer import ProfileResponseSerializer, UpdateProfileSerializer
from user.serializer import ChangePasswordRequestSerializer, SignUpRequestSerializer
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password, make_password
from random_username.generate import generate_username
from django.db.utils import IntegrityError


# Create your views here.
class ProfileAPIs(APIView):

    def get(self, request):
        profile = UsersModel.objects.get(user_id=request.user.user_id)
        serializer = ProfileResponseSerializer(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request):
        profile = UsersModel.objects.get(user_id=request.user.user_id)
        serializer = UpdateProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ChangePasswordAPI(APIView):

    def post(self, request):
        
        serializer = ChangePasswordRequestSerializer(data=request.data)
        if serializer.is_valid():
            user = UsersModel.objects.get(user_id=request.user.user_id)

            if check_password(serializer.data['old_password'], user.password):
                user.set_password(serializer.data['new_password'])
                user.save()
            else:
                return Response({"Error": "Credentials are wrong"}, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({"Message": "Password Changed Successfully"}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class SignUpAPI(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignUpRequestSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.data
            data['username'] = generate_username()[0]
            data['password'] = make_password(data['password'], hasher='default')
            data['is_teacher'] = True if data['user_type'] == 'teacher' else False
            data.pop('user_type')
            try:
                user = UsersModel(**data)
                user.save()
                serializer = ProfileResponseSerializer(user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except IntegrityError:
                return Response({'Error': "Email already exists"}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


