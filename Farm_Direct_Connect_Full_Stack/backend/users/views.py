# Farm Direct Connect
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser, GramSahayak
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer,
    UserUpdateSerializer, GramSahayakSerializer
)
from .permissions import IsFarmer, IsBuyer

class AuthViewSet(viewsets.ViewSet):
    permission_classes = [AllowAny]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                'message': 'User registered successfully',
                'access': str(refresh.access_token),
                'refresh': str(refresh),
                'user': UserProfileSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'])
    def login(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = authenticate(
                username=serializer.validated_data['username'],
                password=serializer.validated_data['password']
            )
            if user and user.role == serializer.validated_data['role']:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message': 'Login successful',
                    'access': str(refresh.access_token),
                    'refresh': str(refresh),
                    'user': UserProfileSerializer(user).data
                }, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return CustomUser.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def profile(self, request):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put'])
    def update_profile(self, request):
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully', 'user': serializer.data})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def farmer_details(self, request):
        farmer_id = request.query_params.get('farmer_id')
        try:
            farmer = CustomUser.objects.get(id=farmer_id, role='farmer')
            serializer = UserProfileSerializer(farmer)
            return Response(serializer.data)
        except CustomUser.DoesNotExist:
            return Response({'message': 'Farmer not found'}, status=status.HTTP_404_NOT_FOUND)


class GramSahayakViewSet(viewsets.ModelViewSet):
    serializer_class = GramSahayakSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=False, methods=['post'])
    def register(self, request):
        try:
            gram_sahayak = GramSahayak.objects.create(
                user=request.user,
                location=request.data.get('location')
            )
            serializer = GramSahayakSerializer(gram_sahayak)
            return Response({
                'message': 'Gram Sahayak registration submitted for approval',
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'message': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def status(self, request):
        try:
            gram_sahayak = GramSahayak.objects.get(user=request.user)
            serializer = GramSahayakSerializer(gram_sahayak)
            return Response(serializer.data)
        except GramSahayak.DoesNotExist:
            return Response({'message': 'No registration found'}, status=status.HTTP_404_NOT_FOUND)