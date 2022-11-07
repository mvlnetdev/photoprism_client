"""Set up a session with the photoprism server"""

import requests, json

class Session():
    def __init__(self, username, password, host):
        """Initialize using a username, password and hostname"""
        self.username = username
        self.password = password
        self.login_data = {
            "username": self.username,
            "password": self.password
        }

        self.host = host
        self.url = f"http://{self.host}/api/v1"

    def create(self):
        """Create the session"""

        r = requests.post(f"{self.url}/session", json.dumps(self.login_data))
        data =  json.loads(r.text)
        self.session_id = data["id"]
        return True

