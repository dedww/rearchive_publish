from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

# Email of the Service Account
SERVICE_ACCOUNT_EMAIL = 'dedwwroot@vstest-1533458347243.iam.gserviceaccount.com'
# Path to the Service Account's Private Key file
SERVICE_ACCOUNT_PKCS12_FILE_PATH = '/home/dedww/rearchive/7bf329b9285dc7aba2029404d0e68e48fad2bcad'

def create_directory_service(user_email):
    """Build and returns an Admin SDK Directory service object authorized with the service accounts
    that act on behalf of the given user.

    Args:
      user_email: The email of the user. Needs permissions to access the Admin APIs.
    Returns:
      Admin SDK directory service object.
    """

    credentials = ServiceAccountCredentials.from_p12_keyfile(
        SERVICE_ACCOUNT_EMAIL,
        SERVICE_ACCOUNT_PKCS12_FILE_PATH,
        'notasecret',
        scopes=['https://www.googleapis.com/auth/admin.directory.user'])

    credentials = credentials.create_delegated(user_email)

    return build('admin', 'directory_v1', credentials=credentials)
