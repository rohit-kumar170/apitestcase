from rest_framework import generics
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .models import CustomUser,Product
from .serializers import RegisterSerializer,ProductSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework import viewsets

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": {
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            }
        }, status=HTTP_201_CREATED)

class CustomLoginView(APIView):
    '''
    {
    "email":"rohit123@gmail.com",
    "password":"Password@123"
    }
    '''
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        
class ProductViewSet(viewsets.ModelViewSet):
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all().order_by('-id')
    serializer_class = ProductSerializer