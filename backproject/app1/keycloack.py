from keycloak import KeycloakAdmin  # Import KeycloakAdmin from keycloak module
import requests.exceptions  # Import requests.exceptions module for handling exceptions

class Keycloak:
    # Initialize KeycloakAdmin instance with appropriate parameters
    kc_admin = KeycloakAdmin(
        server_url="http://localhost:8080/auth/",  # Keycloak server URL
        realm_name='Lead',  # Realm name
        client_id="DjangoPromoteApp1",  # Client ID
        client_secret_key="gvew0FcYxTKAqJ579UikBlONlY2XBTGe",  # Client secret key
        verify=True  # Verify SSL certificate (default is True)
    )
