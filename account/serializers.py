from django.forms import ValidationError
from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User

        fields = ['email', 'name', 'password', 'password2', 'tc']

        extra_kwargs = {'password': {'write_only': True}}

    # validate password and confirm password
    def validate(self, attrs):
        pass1 = attrs.get('password')
        pass2 = attrs.get('password2')
        if pass1 != pass2:
            raise serializers.ValidationError("Password doesn't match")
        return super().validate(attrs)

    def create(self, validate_data):
        return User.objects.create_user(**validate_data)



class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = User
        fields = ['email', 'password']


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'email']







