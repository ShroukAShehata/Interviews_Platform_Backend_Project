from rest_framework import serializers
from .models import User

# Serializer for User model.
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'experience_level', 'bio']
        read_only_fields = ['id', 'role'] 


# Registration class for user sign-up
class UserRegisterSerializer(serializers.ModelSerializer):

    #write_only to ensure password is not returned in responses, but only used for creating user.
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'role']


    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            role=validated_data.get('role', 'learner')
        )
        return user
