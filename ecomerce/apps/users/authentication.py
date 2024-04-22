from datetime import timedelta
from django.utils import timezone
from django.conf import settings
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class ExpiringTokenAuthentication(TokenAuthentication):
    expired = False

    # Indica el tiempo de expiracion del token, devolviendo el tiempo faltante de expiracion
    def expires_in(self, token):
        time_elapsed = timezone.now() - token.created 
        left_time = timedelta(seconds= settings.TOKEN_EXPIRED_AFTER_SECONDS) - time_elapsed
        return left_time

    # Veficica si el tiempo de expiracion finalizo, devolviendo True o False
    def is_token_expired(self, token):
        return self.expires_in(token) < timedelta(seconds = 0)

    # guarda e True o False si el token a expirado o no
    def token_expire_handler(self, token):
        is_expire = self.is_token_expired(token)
        if is_expire:
            self.expired = True
            user = token.user
            token.delete()
            token = self.get_model().objects.create(user = user)
        
        return is_expire, token

    # Autentica las credenciales del usuario por medio del token
    def authenticate_credentials(self, key):
        user,token,message = None, None, None
        try:
            token = self.get_model().objects.select_related('user').get(key = key) 
            user = token.user
        except self.get_model().DoesNotExist:
            message = 'Token invalido.'

        if token is not None:
            if not token.user.is_active:
                message = 'Usuario no activo o eliminado.'
        
            is_expired = self.token_expire_handler(token)
            if is_expired:
                message = 'Token Expirado.'           
        
        return (user, token, message, self.expired)
