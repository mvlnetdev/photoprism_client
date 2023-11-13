from photoprism.Session import Session
from photoprism.Photo import Photo

pp_session = Session("admin", "changethis", "demo.photoprism.app")
pp_session.create()

p = Photo(pp_session)
data = p.start_index(path="/2002", rescan=True)

if type(data) == list:
    print(f"Returned: {len(data)} results")
