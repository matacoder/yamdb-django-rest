from django.conf import settings
from django.contrib.auth import authenticate, get_user_model
from django.core.mail import send_mail
from rest_framework import exceptions, serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken

from .tokens import account_activation_token

User = get_user_model()


class RegistrationSerializer(serializers.ModelSerializer):
    ''' Serializer for registration with a single email field '''

    class Meta:
        model = User
        fields = ('email',)

    def create(self, validated_data):
        '''
        Create a non-activated account for a user.
        Generation of a token for confirmation of registration based on id etc.
        Sending a token to the mail.
        '''
        validated_data['is_active'] = False
        user = User.objects.create_user(**validated_data)
        activation_token = account_activation_token.make_token(user)
        send_mail(
            'YamDB api registration',
            f'Your confirmation code: {activation_token}',
            settings.YAMDB_EMAIL,
            [validated_data['email']],
            fail_silently=False
        )
        return user


class CustomJWTSerializer(serializers.Serializer):
    email = serializers.EmailField()
    confirmation_code = serializers.CharField()

    default_error_messages = {
        'no_active_account': 'No active account found with given credentials'
    }

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        '''
        Token validation and user authorization.
        '''
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError(
                self.default_error_messages
            )

        activation_token = attrs['confirmation_code']
        if account_activation_token.check_token(user, activation_token):
            user.is_active = True
            user.set_password(activation_token)
            user.save()

        if 'request' not in self.context:
            raise serializers.ValidationError(
                self.default_error_messages
            )

        authenticate_kwargs = {
            'email': attrs['email'],
            'password': attrs['confirmation_code'],
            'request': self.context['request'],
        }

        self.user = authenticate(**authenticate_kwargs)

        if self.user is None or not self.user.is_active:
            raise exceptions.AuthenticationFailed(
                self.error_messages['no_active_account'],
                'no_active_account',
            )

        refresh = self.get_token(self.user)

        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        return data


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True, validators=[UniqueValidator(User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'username', 'bio', 'email', 'role'
        )
