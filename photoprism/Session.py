"""Set up a session with the photoprism server"""

import json
from requests import Session as r_session, Request as r_request

from photoprism import mimetypes

class Session():
    def __init__(self, username, password, host, use_https=False, verify_cert=True, user_agent=None):
        """Initialize using a username, password and hostname"""
        self.username = username
        self.password = password
        self.login_data = {
            "username": self.username,
            "password": self.password
        }

        self.host = host

        self.protocol = "http"
        self.ssl_enable = use_https
        if self.ssl_enable:
            self.protocol = self.protocol + "s"
            self.ssl_verify = verify_cert
        self.url = f"{self.protocol}://{self.host}/api/v1"


        self.user_agent = "Photoprism Python Client"
        if user_agent:
            self.user_agent = user_agent

        self.headers = {
            "User-Agent": self.user_agent
        }

    def req(self, endpoint, method, **kwargs):
        s = r_session()
        r = r_request(method=method, url=f"{self.url}{endpoint}")

        if self.ssl_enable:
            s.verify = self.ssl_verify
        r.headers = self.headers

        for k, v in kwargs.items():
            if k == "data":
                r.data = json.dumps(v)

        p = r.prepare()
        resp = s.send(p)

        headers = resp.headers

        content_type = headers["Content-Type"].split("; ")
        if content_type[0] == "application/json":
            data_out = json.loads(resp.text)
        elif content_type[0].split("/")[0] == "image":
            extension = mimetypes.image[content_type[0].split("/")[1]]
            if "filename" in kwargs:
                filename = f"{kwargs['filename']}{extension}"
            else:
                header_filename = headers["Content-Disposition"].split("; ")[1]
                filename = header_filename.split("=")[1][1:-1]

            if "path" in kwargs:
                filename = f"{kwargs['path']}/{filename}"

            with open(filename, "wb") as f:
                resp.raw.decode_content = True
                f.write(resp.content)
            data_out = True

        else:
            data_out = resp.text

        return resp.status_code, data_out

    def create(self):
        """Create the session"""
        _, data = self.req("/session", "POST", data=self.login_data)
        self.session_id = data["id"]
        self.headers["X-Session-ID"] = self.session_id
        return True
