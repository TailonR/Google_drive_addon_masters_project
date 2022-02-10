# What Should This App Do?
## Finishing-touches functionality
* Need to store the resourceID of the channels created
  * May want to have a property that is the file id that the channel is watching
* Have the homepage show the files that are already being tracked
* Have a way to extend the lifetime of the channel
* Show different functionality for the demo on March 1st
* Track changes for directories
* Have different message text for when a file is deleted
* Need to edit the notification card so that it uses proper grammar 
  * for multiple files say "are" and for a single file say "is"

## Future Funcitionality
* Allow users to select a file to watch
* Alert others to changes to the file
  * "Others" meaning people to whom the file is shared
  * or anyone the user wants to alert
  * "Alert" in this case means to notify, either through Gmail or 
  some other service (like Discord)
* Monitor when a file was downloaded
* Alert others to when the file is downloaded
* Automatically delete the file once the download is done
* Fix when credentials are expired and cannot be refreshed (or when none
exist) and how to get the user to reauthorize without getting the error
that they must go to a certain link to authorize
* Make it extensible for new Google drive events or new applications
* Make app

## Questions:
* Is Google Cloud Datastore the best way to store the tokens?
* How do I test?
* How do I save previous page tokens, if sticking with Google Drive API v3?
* How do I cache the google drive change list result? Just use watch?