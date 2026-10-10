from .models import User, NEW, CODE_VERIFIED, VIA_EMAIL, VIA_PHONE
from rest_framework.response import Response
from .serializers import SignUpSerializer, ChangeUserInfoSerializer, ChangeUserPhotoSerializer, LoginSerializer
from rest_framework.generics import CreateAPIView, UpdateAPIView
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from django.utils import timezone
from rest_framework.exceptions import ValidationError
from .utility import send_email, send_phone_code
from rest_framework_simplejwt.views import TokenObtainPairView

class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]
    
class VerifyAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request,  *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')
        
        self.check_verify(user, code)
        token_data = user.token()
        
        return Response(
            data={
                'success':True,
                'auth_status': user.auth_status,
                'access':token_data['access'],
                'refresh': token_data['refresh_token']
            }
        )
    @staticmethod
    def check_verify(user, code):
        verifies = user.verify_codes.filter(expiration_time__gte = timezone.now(), code=code, is_confirmed=False)
        print(verifies)
        if not verifies.exists():
            data = {
                'success':False,
                'message': 'Invalid code'
            }
            raise ValidationError(data)
        else:
            verifies.update(is_confirmed=True)
        if user.auth_status == NEW:
            user.auth_status = CODE_VERIFIED
            user.save()
            
        return True
    
class ResendVerifyCodeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        user = self.request.user
        code = self.request.data.get('code')
        self.check_verification(user)
        if user.auth_type==VIA_EMAIL:
            code = user.generate_verification_code(VIA_EMAIL)
            send_email(user.email, code)
        elif user.auth_type ==VIA_PHONE:
            code = user.generate_verification_code(VIA_PHONE)
            send_email(user.email, code)
            #send_phone_code(user.phone_number, code)
        else:
            data = {
                'success':False,
                'message':'Email or phone number is invalid'
            }
            raise ValidationError(data)
        return Response(
            {
                'success':True,
                'message':'Code has been sent successfully',
            }
        )
    @staticmethod  
    def check_verification(user):
        verifies = user.verify_codes.filter(expiration_time__gte=timezone.now(), is_confirmed=False)
        if verifies.exists():
            data = {
                'success':False,
                "message":"Your code isn't expired yet"
            }
            raise ValidationError(data)
            
class ChangeUserInformationView(UpdateAPIView):
    serializer_class = ChangeUserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]
    http_method_names = ['patch', 'put']
    
    def get_object(self):
        return self.request.user
    
    def update(self, request, *args, **kwargs):
        super().update(request, *args, **kwargs)
        data = {
            'success':True, 
            'message':'User updated successfully',
            'auth_status':self.request.user.auth_status,
        }
        return Response(data, status=200)
    
    def partial_update(self, request, *args, **kwargs):
            super().partial_update(request, *args, **kwargs)
            data = {
                'success':True, 
                'message':'User updated successfully',
                'auth_status':self.request.user.auth_status,
            }
            return Response(data, status=200)
        
class ChangeUserPhotoView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def put(self, request, *args, **kwargs):
        serializer = ChangeUserPhotoSerializer(data=request.data)
        
        if serializer.is_valid():
            user = request.user
            serializer.update(user, serializer.validated_data)
            return Response(
                {
                    'message': 'Photo updated successfully'
                }, status=200
            )
        else:
            return Response(
                serializer.errors, status=400
            )
            
class LoginView(TokenObtainPairView):
    serializer_class = LoginSerializer