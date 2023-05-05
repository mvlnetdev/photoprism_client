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
new_album = p.create_album(temp_name)
print(new_album)

# Add the first photo to the album
foto_uid = p.search(query="original:*", count=1)
print(p.add_photos_to_album([foto_uid[0]["UID"]],new_album["UID"]))

print(p.remove_photos_from_album(albumname=new_album["Title"]))

print(p.add_to_album_from_query(query="original:*", albumname=new_album["Title"], count=1))

# Delete an album
print(p.remove_album(temp_name))