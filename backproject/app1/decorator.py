from keycloak import KeycloakOpenID, exceptions  # Import KeycloakOpenID and exceptions from keycloak module

# Initialize KeycloakOpenID instance
keycloak_openid = KeycloakOpenID(
    server_url="http://localhost:8080/auth/",  # Keycloak server URL
    realm_name="Lead",  # Realm name
    client_id="account",  # Client ID
    verify=True,  # Verify SSL certificate (default is True)
)

from functools import wraps  # Import wraps function from functools module
from django.http import JsonResponse  # Import JsonResponse class from django.http module

# Decorator class
class decorator:
    # Method to require token for accessing endpoints
    def requires_token(func):
        # Wrapper function
        @wraps(func)
        def wrapper(self, request, *args, **kwargs):
            # Retrieve access token from request headers
            access_token = request.headers.get('Authorization')
            print(access_token)
            # If access token is missing
            if not access_token:
                return JsonResponse({'error': 'Authorization header is missing'}, status=401)

            # Extract token value (excluding 'Bearer ')
            access_token = access_token[7:]
            try:
                # Validate token and retrieve userinfo
                userinfo = keycloak_openid.userinfo(access_token)
                # Call the original function with arguments
                return func(self, request, *args, **kwargs)

            # Handle Keycloak errors
            except exceptions.KeycloakError as e:
                return JsonResponse({'error': str(e)}, status=401)

            # Handle other exceptions
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=400)

        return wrapper  # Return the wrapper function
