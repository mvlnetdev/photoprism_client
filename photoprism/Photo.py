"""Interaction with the API of PhotoPrism"""
import uuid

from photoprism import Session
import requests, json

class Photo():
    def __init__(self, session):
        """Initialize based upon a session"""
        if type(session) != Session.Session:
            raise TypeError(f"session variable is not of type photoprism.Session.Session, but {type(session)}")

        self.session = session

    def search(self, query, count=100, offset=0, order="newest"):
        """Basic search function. Returns a Dict object based upon the returned JSON"""
        _, data = self.session.req(f"/photos?count={count}&q={query}&offset={offset}&order={order}", "GET")
        return data

    def get_uid_list_of_search(self, query, count=100, offset=0, order="newest"):
        """Return a list of UIDs based upon the search"""

        photos = self.search(query, count, offset=offset, order=order)
        photolist = []
        for ps in photos:
            photolist.append(ps["UID"])

        return photolist

    def list_albums(self, count=100000):
        """Provide a list of all albums within the photoprism instance, with a max of 100000"""
        _, data = self.session.req(f"/albums?count={count}", "GET")
        return data

    def check_if_album_exists(self, name, create_if_not=False):
        """Small function to check if an album exists"""

        data = self.list_albums()
        for d in data:
            if name == d["Title"]:
                return True

        if create_if_not:
            self.create_album(name)

        return False

    def get_album_uid_by_name(self, name):
        """Get the UID of an album using the name of the album. Be aware, it uses the list_albums function that is limited to 100000 albums"""

        data = self.list_albums()
        uid = None
        for d in data:
            if name == d["Title"]:
                return d["UID"]
        
        return False

    def create_album(self, title):
        """Create an album, returns a boolean if it worked"""
        data = {"Title":title,"Favorite":False}
        status_code, output = self.session.req("/albums", "POST", data=data)

        if status_code == 200:
            return output
        
        return False

    def add_photos_to_album(self, photos, album_uid):
        """Add photos to an album, you will need to provide a list of UIDs of the photos you want to add. Returns True if successfull"""
        data = {
            "photos":photos
        }
        status_code, _ = self.session.req(f"/albums/{album_uid}/photos", "POST", data=data)
        if status_code == 200:
            return True

        return False

    def add_to_album_from_query(self, query, albumname, count=1000000, offset=0, order="newest"):
        """Provide a search query and add all photos that are returned into an album. Provide the albumname, not the UID of the album."""

        self.check_if_album_exists(albumname, create_if_not=True)
        album_uid = self.get_album_uid_by_name(albumname)
        photolist = self.get_uid_list_of_search(query, count=count, offset=offset, order=order)
        result = self.add_photos_to_album(photolist, album_uid)
        return result

    def get_album(self, uid):
        """Get all information of an album based upon the UID of the album"""
        status_code, data = self.session.req(f"/albums/{uid}", "GET")
        if status_code == 200:
            return data

        return False

    def remove_photos_from_album(self, albumname, photos=False, count=1000000):
        """Remove photos from an album, Returns True if successfull"""
        album_uid = self.get_album_uid_by_name(albumname)
        if photos == False:
            query = f"album:\"{albumname}\""
            photos = self.get_uid_list_of_search(query,count=count)

        data = {
            "photos":photos
        }
        status_code, _ = self.session.req(f"/albums/{album_uid}/photos", "DELETE", data=data)
        if status_code == 200:
            return True

        return False

    def remove_album(self, albumname):
        """Remove album based on album name"""
        album_uid = self.get_album_uid_by_name(albumname)
        return self.remove_album_uid(album_uid)

    def remove_album_uid(self, uid):
        """Remove album based on album uid"""
        status_code, data = self.session.req(f"/albums/{uid}", "DELETE")
        if status_code == 200:
            return data

        return False

    def start_import(self, path="upload", move=False):
        """Start an import job, default path is upload. It returns True when the import started, not when finished"""
        data = {
            "path": path,
            "move": move
        }
        status_code, _ = self.session.req(f"/import", "POST", data=data)
        if status_code == 200:
            return True
        
        return False

    def stop_import(self):
        """Stop an import job"""
        status_code, _ = self.session.req("/import", "DELETE")
        if status_code == 200:
            return True
        
        return False

    def start_index(self, path="/", rescan=False, cleanup=False ):
        """Start an import job, default path is /. It returns True when the import started, not when finished"""
        data = {
            "path": path,
            "rescan": rescan,
            "cleanup": cleanup
        }
        status_code, _ = self.session.req(f"/index", "POST", data=data)
        if status_code == 200:
            return True
        
        return False

    def stop_index(self):
        """Stop an index job"""
        status_code, _ = self.session.req("/index", "DELETE")
        if status_code == 200:
            return True
        
        return False

    def download_file(self, hash, path=".", filename=None):
        """Download a single file"""
        status_code, data = self.session.req(f"/dl/{hash}", "GET", path=path, filename=filename)

        if status_code == 200:
            return True
        return False

    def download_album(self, uid, path=".", filename=None):
        """Download an entire album as ZIP"""
        status_code, data = self.session.req(f"/albums/{uid}/dl", "GET", stream=True, path=path, filename=filename)

        if status_code == 200:
            return True
        return False

    def download_files_from_query(self, query, count=100, offset=0, order="newest"):
        """Download files from a query"""
        # In order to make it easy, files are first put into a temporary album
        # After which they are downloaded
        # After the download is complete, the folder is removed.

        temp_album = self.create_album(str(uuid.uuid4()))
        status = self.add_to_album_from_query(query, temp_album["Title"], count=count, offset=offset, order=order)
        status = self.download_album(temp_album["UID"])
        status = self.remove_album_uid(temp_album["UID"])
        return status




