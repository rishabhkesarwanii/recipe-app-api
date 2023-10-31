"""
Serializers for the user API views
"""
from django.contrib.auth import (
    get_user_model,
    authenticate,
    )
from django.utils.translation import gettext as _
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for user object"""

    class Meta:
        model = get_user_model()
        fields = ('email','password', 'name')
        extra_kwargs = {'password':{'write_only':True, 'min_length':5}}
    
    def create(self, validated_data):
        """Create and return a user with encrypted password"""
        return get_user_model().objects.create_user(**validated_data) 
    
    # defualt func of serializer to create object with defuat input no hashing the password
    # we override the create method coz we want to hash the password
    # the create method will only be called if there is validation else it will be called

    def update(self, instance, validated_data):
        """Update a user, setting the password correctly and return it"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


    
class AuthTokenSerializer(serializers.Serializer):
    """Serializer for the user auth token"""
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type':'password'},
        trim_whitespace=False,
    )

    def validate(self, attrs):
        """Validate and authenticate the user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            username = email,
            password = password,
        )

        if not user:
            msg = _('Unable to authenticate and provide credentails')
            raise serializers.ValidationError(msg, code='authorization')
        
        attrs['user'] = user
        return attrs