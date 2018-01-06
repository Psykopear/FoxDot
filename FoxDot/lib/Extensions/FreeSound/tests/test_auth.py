from unittest import mock

from ..auth import open_browser, webbrowser, CLIENT_ID, authenticate


def test_open_browser_works():
    """
    Test that the browser gets opened at the correct url
    """
    with mock.patch.object(webbrowser, 'open') as Mock:
        open_browser()
        Mock.assert_called_once_with(
            'https://freesound.org/apiv2/oauth2/authorize/'\
            '?client_id=%s&response_type=code&state=xyz' % CLIENT_ID)

def test_authenticate():
    authenticate()
