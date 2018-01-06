import json
import os
import requests
import time
import webbrowser

from appdirs import user_config_dir
from datetime import datetime, timedelta
from tkinter import Tk, Label, Entry, Button, W

from . import freesound


class Config:
    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

    def __init__(self):
        """
        Create config dir if needed, read config from file
        """
        self.root = user_config_dir("FoxDot", version="0.5")
        self.path = '{root}/{config_file}'.format(root=self.root, config_file='config.json')

        # Read config file and set instance settings
        config = self.get_config()
        self.access_token = config.get('access_token', '')
        self.refresh_token = config.get('refresh_token', '')
        self.code = config.get('code', '')
        try:
            self.expire = datetime.strptime(config.get('expire', None), self.DATE_FORMAT)
        except TypeError:
            self.expire = None

    def get_config(self):
        """
        Check that config dir exists, get config file, create it if needed
        """
        self.check_dir()
        try:
            config = json.load(open(self.path, 'rb'))
        except FileNotFoundError:
            with open(self.path, 'w') as file:
                json.dump({}, file)
            config = json.load(open(self.path, 'rb'))
        return config

    def check_dir(self):
        """
        Create config dir if it doesn't exists
        """
        try:
            os.makedirs(self.root)
        except FileExistsError:
            # directories already exist, everything ok
            pass

    def write_to_file(self):
        """
        Dump config to file, converting datetime to string
        """
        with open(self.path, 'w') as file:
            json.dump({
                'access_token': self.access_token,
                'expire': self.expire.strftime(self.DATE_FORMAT),
                'refresh_token': self.refresh_token,
                'code': self.code,
            }, file)


class AuthException(Exception):
    """
    Exception raised when there are missing environment variables
    """
    pass


class Auth:
    """
    Class to hold authorization tokens and handle token refresh
    Needs FREESOUND_CLIENT_ID and FREESOUND_CLIENT_SECRET environment
    variables to be set
    """

    ACCESS_TOKEN_URL = 'https://freesound.org/apiv2/oauth2/access_token/'
    AUTHORIZE_URL = 'https://freesound.org/apiv2/oauth2/authorize/?client_id={client_id}&response_type=code&state=xyz'

    def __init__(self, cli=True):
        """
        Client id and client secret should be retrieved from freesound.org,
        in the developer section of the website.
        If the `cli` parameter is set to True, no Gui will be used
        """
        self.client_id = os.getenv("FREESOUND_CLIENT_ID")
        if not self.client_id:
            raise AuthException("You must set FREESOUND_CLIENT_ID environment variable!")

        self.client_secret = os.getenv("FREESOUND_CLIENT_SECRET")
        if not self.client_secret:
            raise AuthException("You must set FREESOUND_CLIENT_SECRET environment variable!")

        self.cli = cli
        self.config = Config()

        # Start the authentication process
        self.authenticate()

    def get_code(self):
        """
        Get the code returned by freesound, via Tk gui if cli is False,
        or via user input if cli is True
        """
        if not self.cli:
            # XXX: Buggy at the moment, should be integrated in foxdot's gui
            # master = Tk()
            # Label(master, text="Code").grid(row=0)
            # e = Entry(master)
            # e.grid(row=0,column=1)
            # Button(master, text='Confirm', command=master.quit).grid(row=2,column=1, sticky=W, pady=4)
            # master.mainloop()
            # return e.get()

            # XXX: We just ignore the cli argument at the moment
            return input("Insert code: ")
        else:
            return input("Insert code: ")

    def open_browser(self):
        """
        Open browser at the authorize url so the user can login
        and retrieve the token needed to make calls
        """
        webbrowser.open(self.AUTHORIZE_URL.format(client_id=self.client_id))

    def get_token(self, code, refresh=False):
        """
        Get the access token
        """
        res = requests.post(
            self.ACCESS_TOKEN_URL,
            data={
                "client_id": self.client_id,
                "client_secret": self.client_secret,
                "grant_type": "refresh_token" if refresh else "authorization_code",
                "code": code
        })
        data = res.json()
        self.config.access_token = data['access_token']
        self.config.expire = datetime.now() + timedelta(seconds=data['expires_in'])
        self.config.refresh_token = data['refresh_token']
        self.config.code = code
        self.config.write_to_file()


    def _auth(self):
        """
        Authentication process used the first time, or when both access_token
        and refresh_token are not valid anymore
        """
        self.open_browser()
        code = self.get_code()
        self.get_token(code)

    def refresh(self):
        """
        Get new token using refresh token
        """
        self.get_token(self.config.refresh_token, refresh=True)

    def authenticate(self):
        """
        Authentication flow:
            Open browser so the user can login and get a token
            Let the user insert the received token
            Make a request to freesound.org to retrieve our access_token
        """
        if self.config.access_token:
            if (self.config.expire - datetime.now()).total_seconds() < 0:
                try:
                    self.refresh()
                except Exception:
                    self._auth()
        else:
            self._auth()
