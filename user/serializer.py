from rest_framework import serializers
from user.models import UsersModel

class ProfileResponseSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersModel
        fields = ['user_id', 'username', 'email', 'is_teacher', 'profile_pic', 'created_at']


class UpdateProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = UsersModel
        fields = ['username', 'email', 'profile_pic']


class ChangePasswordRequestSerializer(serializers.Serializer):

    old_password = serializers.CharField(max_length=100)
    new_password = serializers.CharField(max_length=100)

    def validate(self, attrs):
        if attrs['old_password'] == attrs['new_password']:
            raise serializers.ValidationError(
                detail="New Password must be different than old password")


class SignUpRequestSerializer(serializers.Serializer):
    
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    user_type = serializers.ChoiceField(choices=['student', 'teacher'])
    profile_pic = serializers.CharField(max_length=100, allow_blank=True)


