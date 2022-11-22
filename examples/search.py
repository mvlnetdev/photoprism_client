from photoprism.Session import Session
from photoprism.Photo import Photo

pp_session = Session("admin", "changethis", "demo.photoprism.app")
pp_session.create()

p = Photo(pp_session)
p.search(query="original:*")