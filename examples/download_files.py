from photoprism.Session import Session
from photoprism.Photo import Photo

pp_session = Session("admin", "changethis", "demo.photoprism.app")
pp_session.create()

p = Photo(pp_session)
data = p.search(query="original:*", count=1)

p.download_file(data[0]["Hash"])

data = p.list_albums(count=1)
p.download_album(uid=data[0]["UID"])

p.download_files_from_query(query="original:*", count=1)