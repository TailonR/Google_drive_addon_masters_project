# What Should This App Do?
## Finishing-touches functionality
* Change the container image from helloworld stuff to file watch stuff
* Have a way to extend the lifetime of the channel (partially solved with track-item)
* Have a way for users to add an email to an already tracked file
* Have different message text for when a file is deleted

## Future Functionality
* Alert others to changes to the file
  * "Others" meaning people to whom the file is shared
  * or anyone the user wants to alert
  * "Alert" in this case means to notify, either through Gmail or 
  some other service (like Discord)
* Monitor when a file was downloaded
  * Can possibly be done by allowing users to download the content 
    webContentLink of the file through the app,
    as shown by this YouTube video https://youtu.be/1y0-IfRW114?t=1303
  * Then keeping track of when the requests were made
  * The video is done in Node.js so going to have to figure out how to do it
    in Python
* Alert others to when the file is downloaded
* Automatically delete the file once the download is done
* Fix when credentials are expired and cannot be refreshed (or when none
exist) and how to get the user to reauthorize without getting the error
that they must go to a certain link to authorize
* Make it extensible for new Google Drive events or new applications
* Make app

## Questions:
* Is Google Cloud Datastore the best way to store the tokens?
* How do I test?
* How do I save previous page tokens, if sticking with Google Drive API v3?
* How do I cache the Google Drive change list result? Just use watch?