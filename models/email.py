from apiclient import discovery


class Email:

    """Get user email from OAuth2 service."""

    def __init__(self, http_auth):
        self.http_auth = http_auth

    def discover_user(self):
        user_info_service = discovery.build(serviceName='oauth2',
                                            version='v2',
                                            http=self.http_auth)
        user_info = user_info_service.userinfo().get().execute()
        return user_info
