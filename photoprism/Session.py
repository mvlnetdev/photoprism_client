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

    def req(self, endpoint, method, stream=False, **kwargs):
        s = r_session()

        url = f"{self.url}{endpoint}"
        if endpoint[-3:] == "/dl":
            url = f"{self.url}{endpoint}?t={self.download_token}"

        r = r_request(method=method, url=url)

        if self.ssl_enable:
            s.verify = self.ssl_verify
        r.headers = self.headers

        for k, v in kwargs.items():
            if k == "data":
                r.data = json.dumps(v)

        p = r.prepare()
        resp = s.send(p, stream=stream)

        headers = resp.headers
        content_type = headers["Content-Type"].split("; ")
        mime_type, mime_subtype = content_type[0].split("/")

        # Process the return data
        if mime_type == "application":
            if mime_subtype == "json":
                data_out = json.loads(resp.text)
            elif mime_subtype == "zip":
                filename = self.determine_filename(kwargs, mime_type, mime_subtype, headers)
                with open(filename, 'wb') as f:
                    for chunk in resp.iter_content(chunk_size=10240):
                        f.write(chunk)
                data_out = True
            else:
                data_out = resp.text

        # Process downloaded single files
        elif mime_type in ["image", "video"]:
            filename = self.determine_filename(kwargs, mime_type, mime_subtype, headers)

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
        self.download_token = data['config']['downloadToken']

        return True

    def determine_filename(self, args, mime_type, mime_subtype, headers):
        if args["filename"] != None:
            extension = mimetypes.type[mime_type][mime_subtype]
            filename = f"{args['filename']}{extension}"
        else:
            header_filename = headers["Content-Disposition"].split("; ")[1].split("=")[1]
            # Sometimes the filename in the header is enclosed, sometimes it isn't. This is to account for that.
            if header_filename[0] == '"' and header_filename[-1:] == '"':
                filename = header_filename[1:-1]
            else:
                filename=header_filename

        if "path" in args:
            filename = f"{args['path']}/{filename}"

        return filename
