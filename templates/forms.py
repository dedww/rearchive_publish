from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, InputRequired, ValidationError
import requests
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from oauth2client.client import OAuth2WebServerFlow
from requests.auth import HTTPBasicAuth

# If modifying these scopes, delete the file token.json.
# SCOPES = 'https://www.googleapis.com/auth/admin.directory.user'
SCOPES = ['https://www.googleapis.com/auth/admin.directory.member', 'https://www.googleapis.com/auth/admin.directory.member']

groupKey = "dedwwtest@googlegroups.com"

def check(FlaskForm, field):
    """Shows basic usage of the Admin SDK Directory API.
       Prints the emails and names of the first 10 users in the domain.
       """
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    path = '/home/dedww/rearchive/templates/'
    store = file.Storage(path+'token.json')
    creds = store.get()

    if not creds or creds.invalid:
        flow = client.flow_from_clientsecrets(path+'credentials.json', SCOPES)
        creds = tools.run_flow(flow, store)
    service = build('admin', 'directory_v1', http=creds.authorize(Http()))

    url = requests.get("https://www.googleapis.com/admin/directory/v1/groups/" + groupKey + "/hasMember/" + field.data)
    c = requests.get('https://www.googleapis.com/discovery/v1/apis')
    response = requests.get(
        'https://www.googleapis.com/admin/directory/v1/groups/' + groupKey + 'hasMember/' + field.data)

    #if response.status_code == 401:
     #   response = requests.get(
      #      'https://www.googleapis.com/admin/directory/v1/groups/' + groupKey + '/hasMember/' + field.data,
       #     auth=HTTPBasicAuth('user', 'pass'))
    print(response)
    if url != "True":
        raise ValidationError('This mail hasnt connection to googlegroup')

class LoginForm(FlaskForm):
    username = StringField('@gmail', validators=[InputRequired(), check])
    # password = PasswordField('Password', validators=[DataRequired()])
    # remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
