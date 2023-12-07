from rest_framework import serializers
from api.models import MyUserManager,MyUser
from django.utils.encoding import smart_str,force_bytes,DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from . utils import util


class UserRegistrationSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type': 'password'})
    
    class Meta:
        model = MyUser
        fields = ['email', 'date_of_birth', 'password', 'password2',]
        extra_kwargs = {
            'password': {'write_only': True}
        }
        
    def validate(self, attrs):
        password = attrs.get('password')
        password1 = attrs.get('password2')
        if password != password1:
            raise serializers.ValidationError("Password and confirm password don't match")
        return attrs
        
    def create(self, validated_data):
        validated_data.pop('password2', None)  # Remove password2 from validated_data
        return MyUser.objects.create_user(**validated_data)
    
class UserLoginSerializers(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255)
    class Meta:
        model=MyUser
        fields=["email","password"]
        
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model=MyUser
        fields="__all__"
    
class ChangePasswordSerializer(serializers.Serializer):
    password1=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    password2=serializers.CharField(max_length=255,style={'input_type':'password'},write_only=True)
    class Meta:
        fields=['password1',['password2']]
        
    def validate(self, attrs):
        password1=attrs.get('password1')
        password2=attrs.get('password2')
        user=self.context.get('user')
        if password1 != password2:
            raise serializers.ValidationError("password doesn't match")
        user.set_password(password1)
        user.save()
        
        return attrs
        
class ResetEmailSerializer(serializers.Serializer):
    email=serializers.CharField(max_length=255)
    class Meta:
        fields=['email']
    def validate(self, attrs):
        email=attrs.get('email')
        if MyUser.objects.filter(email=email).exists():
            user=MyUser.objects.get(email=email)
            uid=urlsafe_base64_encode(force_bytes(user.id))
            print("user id is",uid)
            token=PasswordResetTokenGenerator().make_token(user)
            print('Password Reset',token)
            link='http://127.0.0.1:3000/api/user/reset/'+uid+'/'+token
            print('Password Reset Link',link)
            body='Click here to change your password'+link
            data={
                'subject':'Reset Your Password',
                'body':body,
                'to_email':user.email
            }
            util.send_email(data)
        else:
            return serializers.ValidationError("You are not registered in this app")
        
         
            
        return attrs
    
class ResetPasswordSerializer(serializers.Serializer):
    password1=serializers.CharField(max_length=50)
    password2=serializers.CharField(max_length=50)
    class Meta:
        fields=['password1','password2']
        
    def validate(self, attrs):
        password1=attrs.get('password1')
        password2=attrs.get('password2')
        uid=self.context.get('uid')
        token=self.context.get('token')
        if password1 != password2:
           raise serializers.ValidationError("Password Doesn't Match")
        id=smart_str(urlsafe_base64_decode(uid))
        user=MyUser.objects.get(id=id)
        if not PasswordResetTokenGenerator().check_token(user,token):
            raise serializers.ValidationError("Token is not Valid or Expired")
        user.set_password(password1)
        user.save()
        return attrs
        
            
            
        
        
        
        
            
        
        