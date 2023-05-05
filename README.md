# Python client for PhotoPrism 
A Python client to interact with photoprism.

## IMPORTANT
This Python client is build on the undocumented API of PhotoPrism. There may be bugs in there. Please let me know if you find some. 

Currently tested on the [version of the 17th of June 2022](https://github.com/photoprism/photoprism/releases/tag/220617-0402b8d3). It will probably work with later versions. Just try it and let me know, I will update the readme accordingly.  

## Requirements
- requests (latest)

## Setup
To start interacting with Photoprism set up a session. You always need to do this if you start the script. Otherwise there is no session for the client to interact with PhotoPrism.
``` python
from photoprism.Session import Session
pp_session = Session("admin", "changethis", "demo.photoprism.app")
pp_session.create()
```

### HTTPS
It is possible to connect to Photoprism using HTTPS. Two variables exist for this:
- use_https: Boolean
- verify_cert: Boolean

By default, a connection will be made using HTTP. A session can be set up using HTTPS by setting the use_https variable to _True_. By default the certificate will be verified. This check can be disabled by setting the verify_cert variable to _False_. Only change this if you understand what this means. It is better to leave this variable unchanged. 

An example is:
```python
from photoprism.Session import Session
pp_session = Session("admin", "changethis", "demo.photoprism.app", use_https=True, verify_cert=False)
pp_session.create()
```

### User agent
The user agent is _Photoprism Python Client_ by default. You can change this using the variable _user_agent_. 
For example:
```python
from photoprism.Session import Session
pp_session = Session("admin", "changethis", "demo.photoprism.app", user_agent="Hello World! This is an example.")
pp_session.create()
```

## Searching
To search for photos. With this example it will return the first 100 results. You can change this with `count=1000`.

```python
from photoprism.Photo import Photo

p = Photo(pp_session)
p.search(query="original:*")
```

## Other functions
This is a list of all other functions within the client. If you want other functions either request them or send a pull request.
| function | description | variables | returns |
| ---- | ----- | ------ | ----- |
| Photo.add_photos_to_album() | Add photos to an album, you will need to provide a list of UIDs of the photos you want to add. Returns True if successfull | photos: list, album_uid: string | True if successfull  |
| Photo.add_to_album_from_query() | Provide a search query and add all photos that are returned into an album. Provide the albumname, not the UID of the album. | query: string, albumname: string, count: int (default=1000000) | True if successfull |
| Photo.check_if_album_exists() | Small function to check if an album exists | name: string, create_if_not: bool (default is False) | True if it exists, False if not (will continue to be False if the album is created) |
| Photo.create_album() | Create an album, returns a boolean if it worked | title: string | Dict object with the album information |
| Photo.get_album() | Get all information of an album based upon the UID of the album | uid: string | Dict object with the information of the album, False if it does not exist |
| Photo.get_album_uid_by_name() | Get the UID of an album using the name of the album. Be aware, it uses the list_albums function that is limited to 100000 albums | name: string | String of uid, None if it does not exist |
| Photo.get_uid_list_of_search() | Return a list of UIDs based upon the search | query: string, count: int (default is 100) | list of uids |
| Photo.list_albums() | Provide a list of all albums within the photoprism instance, with a max of 100000 | None | Dict object with all albums and their metadata (max of 100000 results) |
| Photo.raw_call() | Function to perform a request to the photoprism server (usually not needed by a user) | endpoint: string, type: string (default="GET"), data: string (default=False) | requests object |
| Photo.search() | Create the session | query: string, count: int (default=100), offset: int (default=0), order: string (default="newest") | Dict object of the results of the search |
| Photo.start_import() | Start an import job, default path is upload. It returns True when the import started, not when finished | path: string (default="upload"), move: Bool (default=False) | True if successfully started |
| Photo.stop_import() | Stop an import job | None | True if successfully stopped |
| Photo.remove_photos_from_album() | Remove photos from an album, Returns True if successfull | albumname: string, photos: bool (default=False), count: int (default=1000000) | True if succesfull |
| Photo.remove_album() | Remove album based on album name | albumname: string | Dict data returned from the server |

## License 
MIT License

Copyright (c) 2022 maartenvl

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
