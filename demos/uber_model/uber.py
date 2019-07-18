import os
from yaml import safe_load, safe_dump

from uber_rides.auth import AuthorizationCodeGrant
from uber_rides.errors import ClientError, UberIllegalState
from uber_rides.client import UberRidesClient
from uber_rides.session import Session, OAuth2Credential

CREDENTIALS_FILENAME = 'config.rider.yaml'

def import_app_credentials(filename=CREDENTIALS_FILENAME):
    """Import app credentials from configuration file.
    Parameters
        filename (str)
            Name of configuration file.
    Returns
        credentials (dict)
            All your app credentials and information
            imported from the configuration file.
    """
    with open(filename, 'r') as config_file:
        config = safe_load(config_file)

    client_id = config['client_id']
    client_secret = config['client_secret']
    redirect_url = config['redirect_url']

    config_values = [client_id, client_secret, redirect_url]

    # for value in config_values:
    #     if value in DEFAULT_CONFIG_VALUES:
    #         exit('Missing credentials in {}'.format(filename))

    credentials = {
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_url': redirect_url,
        'scopes': set(config['scopes']),
    }

    return credentials


def get_uber_rides_client(credential_storage_file_name):
    credentials = import_app_credentials('config.rider.yaml')

    auth_flow = AuthorizationCodeGrant(
        credentials.get('client_id'),
        credentials.get('scopes'),
        credentials.get('client_secret'),
        credentials.get('redirect_url'),
    )

    auth_url = auth_flow.get_authorization_url()
    login_message = 'Login as a rider and grant access by going to:\n\n{}\n'
    login_message = login_message.format(auth_url)
    print(login_message)

    redirect_url = 'Copy the URL you are redirected to and paste here: \n\n'
    result = input(redirect_url).strip()

    try:
        session = auth_flow.get_session(result)

    except (ClientError, UberIllegalState) as error:
        print("Error getting authorization session.")
        raise SystemExit(error)

    credential = session.oauth2credential

    credential_data = {
        'client_id': credential.client_id,
        'redirect_url': credential.redirect_url,
        'access_token': credential.access_token,
        'expires_in_seconds': credential.expires_in_seconds,
        'scopes': list(credential.scopes),
        'grant_type': credential.grant_type,
        'client_secret': credential.client_secret,
        'refresh_token': credential.refresh_token,
    }

    with open(credential_storage_file_name, 'w') as yaml_file:
        yaml_file.write(safe_dump(credential_data, default_flow_style=False))

    return UberRidesClient(session, sandbox_mode=True)



if __name__ == "__main__":
    # California Academy of Sciences
    START_LAT = 37.770
    START_LNG = -122.466

    # Uber HQ
    END_LAT = 37.7752315
    END_LNG = -122.418075

    file_name = "oauth_rider_session_store.yaml"

    if os.path.exists('oauth_rider_session_store.yaml'):
        pass

    # client = get_uber_rides_client('oauth_rider_session_store.yaml')
    credentials = import_app_credentials('config.rider.yaml')

    oauth = OAuth2Credential(client_id=credentials["client_id"], scopes=credentials["scopes"], access_token=ACCESS_TOKEN, expires_in_seconds=500, grant_type="authorization_code")
    print(oauth)
    session = Session(oauth2credential=oauth)
    client = UberRidesClient(session)


    estimate = client.estimate_ride(
        product_id='d4abaae7-f4d6-4152-91cc-77523e8165a4',
        start_latitude=START_LAT,
        start_longitude=START_LNG,
        end_latitude=END_LAT,
        end_longitude=END_LNG,
        seat_count=2
    )

    print(estimate)

    print(credentials["scopes"])

    estimate = client.get_price_estimates(start_latitude=START_LAT,
        start_longitude=START_LNG,
        end_latitude=END_LAT,
        end_longitude=END_LNG,
        seat_count=2)

    print(estimate)





