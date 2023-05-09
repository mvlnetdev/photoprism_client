# Changelog
Latest update: May 9th 2023
## Version 0.2
### Additions
- Added a count for Photo.add_to_album_from_query() for a maximum count that are from the query, default is 1000000.
- The ability to download files and albums has been added:
	- Photo.download_files(): Download a single file.
	- Photo.download_album(): Download an entire album as ZIP.
	- Photo.download_files_from_query(): Download files from a query.
- Added the ability to force the use of HTTPS. As per request of: [cluk33](https://github.com/cluk33) ([issue #3](https://github.com/mvlnetdev/photoprism_client/issues/3))
- Added offset en order variables to Photo.search() ([PR #4](https://github.com/mvlnetdev/photoprism_client/pull/4) and [PR #5](https://github.com/mvlnetdev/photoprism_client/pull/5)). Thanks [frascu](https://github.com/frascu)!
- Added two functions to remove a photo from an album and to remove an album ([PR #2](https://github.com/mvlnetdev/photoprism_client/pull/2)).  Thanks [sajben94](https://github.com/sajben94)!
- Added the ability to change the User Agent.

### Miscellaneous
- Photo.create_album() now returns a dict object of the newly created album.
- examples/manage_albums.py now contains all functions for albums.
- examples/download_files.py is added to show examples to download files.

