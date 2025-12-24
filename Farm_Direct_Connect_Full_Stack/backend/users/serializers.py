# Farm Direct Connect
from rest_framework import serializers
from .models import CustomUser, GramSahayak

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password_confirm', 'phone', 'role', 
                  'state', 'district', 'address', 'farm_name']
    
    def validate(self, data):
        if data['password'] != data.pop('password_confirm'):
            raise serializers.ValidationError("Passwords do not match")
        return data
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    role = serializers.ChoiceField(choices=['farmer', 'buyer'])


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'phone', 'role', 'state', 'district', 
                  'address', 'farm_name', 'profile_image', 'bio', 'average_rating', 
                  'total_reviews', 'created_at']
        read_only_fields = ['id', 'average_rating', 'total_reviews', 'created_at']


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'phone', 'state', 'district', 'address', 'farm_name', 
                  'profile_image', 'bio', 'latitude', 'longitude']


class GramSahayakSerializer(serializers.ModelSerializer):
    user = UserProfileSerializer(read_only=True)
    
    class Meta:
        model = GramSahayak
        fields = ['id', 'user', 'location', 'farmers_helped', 'products_listed', 
                  'earnings', 'status', 'created_at']
        read_only_fields = ['id', 'farmers_helped', 'products_listed', 'earnings', 'created_at']