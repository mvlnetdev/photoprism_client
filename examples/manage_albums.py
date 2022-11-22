import uuid
from photoprism.Session import Session
from photoprism.Photo import Photo

pp_session = Session("admin", "changethis", "demo.photoprism.app")
pp_session.create()

p = Photo(pp_session)

# List all albums
albums = p.list_albums()

# Check if an album exists
if p.check_if_album_exists("This album probably does not exists") == False:
    print("Does not exists")
else:
    print("It does exist")

# Show the info of an album
album_uid=albums[0]["UID"]
print(f"The name of the first album is: {p.get_album(album_uid)['Title']}")

# Create an album
temp_name=str(uuid.uuid4())
p.create_album(temp_name)

# Delete an album
p.remove_album(temp_name)