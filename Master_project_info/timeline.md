# Master Project Timeline  
**Date: August 24th 2021**  
**Author: Tailon Russell**

This is the timeline for the development of the Master project from 
the creation of the idea through the development of the project.

### May 6th, 2021 
Developed the original idea and noted the new ideas 
that Lawlor presented. 

### May 8th, 2021 
I created the document “Ideas”. 

### August 24th, 2021 
Discussed with CJ Emerson the possibility of using automation for 
content management and deleting old files. Another option 
discussed was working with KSUA in automating the process of 
uploading audio to KSUA and playing it in automation. 

### August 25, 2021 
Discussed with Kevin Swenson about working with KSUA on automating 
the automation process (uploading audio and loading it into zetta). 
Turns out there is quite a bit of automation already. When audio is 
uploaded to the Recently Uploaded, that audio is downloaded into a 
folder of the same name. Then Gselector looks at that file’s 
metadata and compares it with other files that were previously 
loaded that are associated with the volunteer’s show (these are 
called links). If the metadata is new and it is the most recent 
file in the recently uploaded, then it is uploaded to zetta. The 
only human input is scheduling the show for the right time. This is 
more of a sanity check so that there weren’t any mistakes made. 

Kevin S. also noted that other projects that could be useful to KSUA 
is automatically recording shows. The parameters are to start 
recording at the top of the hour, keep the audio for a month, and 
then delete the file. 

Another idea that Kevin S. talked about was 
creating a “plugin” for Zetta for filling out data for configuring 
files. 

### August 26, 2021 
I first looked at a [The Podcast Host article](https://www.thepodcasthost.com/planning/automation-systems-set-you-free/) 
for how to automate the podcast workflow. However, I kept thinking 
about the fact that this is all too simple, not easy necessarily, 
but simple. The problem with the idea is that it is around creating 
something that is not technically complex, which at the least, is 
what a Master’s project and thesis is supposed to focus on. 

While thinking about this I came across the topic of automation 
using AI. I first discovered an [IBM article on automation](https://www.ibm.com/cloud/automation) 
which displayed the ways they used AI in automation. I then 
discovered this article which discusses trends in the use of AI. 

Other supporting articles found: 
* https://pdf.abbyy.com/learning-center/what-is-ocr/ 
* https://moov.ai/en/blog/optical-character-recognition-ocr/ 
* https://planningtank.com/computer-applications/impact-artificial-intelligence-data-collection

### August 30, 2021
I started looking into automation in media. I found a [research paper](https://quod.lib.umich.edu/m/mij/15031809.0001.107/--on-automation-in-media-industries-integrating-algorithmic?rgn=main;view=fulltext#N18) 
about automation in media.

### August 31, 2021
I read the article that I found, and it discussed two roles of 
automation in media: demand predictor and content creation. I 
read a little bit of the demand predictor section and that was 
a bit outside what I was looking to do.  I read the content 
creation section and it led me to a start-up known as [Narrative 
Science](https://narrativescience.com/). This could be something 
that I could look into. It is still a bit outside the scope of 
the project, but it is early enough that I could pivot to 
creating content for podcasters. 

I met with Chappell after CS 690. His recommendations were to 
think about how to specify what happens when an event is 
triggered. This means how is the application going to determine 
what to do when an event happens. Is it going to be a file that 
lists the commands? Is it a GUI? Is it a script? He also told me 
to talk about how the Google Drive API works for talk #0. He also 
told me to send a copy of the document for him to review by Sunday 
so there is some time before I have to present it to address 
anything that he suggests. 

CJ also told me about GPT 3 as a company that has done research in 
generating summaries (essentially what my second idea is). 

### September 1, 2021
Went through Google’s docs for using the Google Drive API. 
The links that walked me through this (in order of date accessed):
1. https://developers.google.com/drive/api/v3/about-sdk
2. https://developers.google.com/drive/api/v3/quickstart/js
3. https://developers.google.com/workspace/guides/create-project
4. https://developers.google.com/workspace/guides/create-credentials
5. https://support.google.com/cloud/answer/6158849#zippy=

I came across an error when first following the Quickstart instructions. 
In the docs it first says that following the Quickstart guide you will 
create a JavaScript web application and the prerequisites say to create 
authorization credentials for a desktop application. So, when I went to 
the “Create Credentials” page I followed the instructions for creating 
Oauth credentials for a “desktop application” (an application type option). 
Then when I ran the server and loaded it in the browser, I got an error 
saying I did not have a valid origin for the client. I found a Stack 
Overflow answer saying to add a JavaScript origins value for the localhost 
URI. However, if I read the instructions for creating Oauth credentials 
closer, I would’ve seen that the Oauth credentials for desktop app was 
only for non-JavaScript applications (this is listed in parenthesis). 
The application for JavaScript applications (such as the Quickstart) was 
the “web application” option. When I created a new Oauth key then the 
application worked (displaying a list of names of some files).

Then I started learning about the authorization process. I followed [the authorization docs](https://developers.google.com/drive/api/v3/about-auth) 
for this.

> Your application must use [OAuth 2.0](https://developers.google.com/identity/protocols/OAuth2) 
> to authorize requests. No other authorization protocols are supported. 
> If your application uses [Google Sign-In](https://developers.google.com/identity/#google-sign-in), 
> some aspects of authorization are handled for you…. All requests to 
> the Drive API must be authorized by an authenticated user.” – Google

I looked up GTP 3 and the closest thing I found was [writing full emails from key points](https://gpt3.website/). 
I also found an [IBM article](https://www.ibm.com/cloud/learn/natural-language-processing) 
about Natural Language Processing (NLP). This article took me to another 
[IBM article about the differences NLP, NLU, and NLG](https://www.ibm.com/blogs/watson/2020/11/nlp-vs-nlu-vs-nlg-the-differences-between-three-natural-language-processing-concepts/). 
Markov Chains are used in Natural Language Understanding (NLU) and Natural 
Language Generation (NLG). 

> The best text summarization applications use semantic reasoning and natural 
> language generation (NLG) to add useful context and conclusions to summaries. 
> – IMB article on NLP.

I then found [a Medium article](https://medium.datadriveninvestor.com/simple-text-summarizer-using-nlp-d8aaf5828e68) 
talking about creating a text summarizer using Python's NLP toolkit. 

### September 2, 2021
I started writing my talk #0 paper.

### September 3, 2021
I continued working on my talk #0 paper. 

I installed Miniconda and PyCharm to use a virtual environment in Pycharm, 
like I had done for work at ASF over the summer. 

I tried to access the API using Python and I ran to an issue with the 
credentials.json file not existing. After reading the instructions, it said 
nothing about creating that file, however, I figured out the credentials file 
is the file that we are given the option to download once we make a Oauth 
Client ID. I downloaded the one for the JavaScript Quickstart instructions, 
renamed it to “credentials” (also added the file to the working directory), 
ran the program again, and that failed. I then figured out that I needed to 
create an Oauth Client ID for a desktop app (an application type option) and 
downloaded that, renamed it, ran the program again, and it worked. It printed 
the same things as the JavaScript Quickstart but instead printed them to the 
console. 

I also discovered the power of GPT-3 and it made me realized that if I could 
incorporate that into the project, I don’t have to worry about creating a NLG, 
just shaping it to fit the desired customers. 

I finished my talk #0 paper.

### September 7, 2021
Gave my talk #0 and met with Chappell who told me to let this simmer for a week 
and then talk about how I want to proceed. 

### September 10, 2021
Learned about “Exactly-once processing” and it’s use in Google Cloud Platform 
pub/sub. I also went to the [pubsublite quickstart](https://cloud.google.com/pubsub/lite/docs/quickstart). 
But got stopped because it required billing. However, I then continued because
the Quickstart provided instructions for unprovisioning resources to avoid 
charges. 

I figured out that I needed to add an environment variable by editing the 
configurations and adding the “GOOGLE_APPLICATION_CREDENTIALS” and included 
the file extension to the file path in value field. 

### September 13, 2021
I looked up creating a google app using Google Cloud Platform and App Engine. 
The Quickstart for this tutorial for App Engine is on the right sidebar of 
the App Engine Dashboard. 

I also determined that what I want to create is a Google Drive plugin. 

### September 14, 2021
I searched for how to create a Google Drive plugin and found [this Google article](https://developers.google.com/workspace/add-ons/how-tos/building-gsuite-addons)
on building gsuite addons. 

Other articles found when researching:
 * Google's tips for UX design: https://developers.google.com/workspace/add-ons/guides/gsuite-style
 * Installing Google Cloud SDK for use with Miniconda's python: https://medium.com/swlh/installing-google-cloud-sdk-to-use-python-from-anaconda-94890014e4e8
   * Learned that I had to restart PyCharm to fix the issue described in step 4
 * Google Cloud SDK Quickstart: https://cloud.google.com/sdk/docs/quickstart

Chappell informed me that I would need to develop a file that would edit a 
config.json file if I wanted to create a GUI for this app. This config.json 
file is the file that contains who needs to be notified, what files need to 
be monitored, and what service they want the message to be sent to. So I will
start off with just having a predefined config file and then possibly 
incorporate a GUI if I have time. 

Links I found today:
* https://bulldogjob.com/news/449-how-to-write-a-good-readme-for-your-github-project
* https://www.figma.com/file/6H3A68mSgD4pJa44v5i5Vb/G-Suite-Add-Ons-UI-Design-Kit-(Community)?node-id=84%3A3202
* https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet
* https://cloud.google.com/sdk/auth_success

### September 16, 2021 
Started working on how to push code to Google, since I don't want to use the 
Cloud Shell Editor, which might just be what I have to do in the end. [This article ](https://cloud.google.com/source-repositories/docs/pushing-code-from-a-repository)
discusses pushing to Cloud Source Repositories. I was able to simply connect to 
the GitHub repository rather than recreating the repository in Cloud Source 
Repositories (after finding [this article](https://cloud.google.com/source-repositories/docs/creating-an-empty-repository)).

I also installed Code Build in this repository. I did this in order to set 
up Cloud Run.

I kept getting an error saying there was a missing "res" argument. Then I found 
[an article](https://cloud.google.com/functions/docs/writing/http#writing_http_helloworld-python) about HTTP functions 

Links found today:
* https://developers.google.com/workspace/add-ons/concepts/homepages
* https://developers.google.com/workspace/add-ons/drive/building-drive-interfaces
* https://developers.google.com/workspace/add-ons/concepts/gsuite-manifests
* https://developers.google.com/workspace/add-ons/reference/rpc/google.apps.card.v1
* https://developers.google.com/workspace/add-ons/guides/alternate-runtimes
* https://developers.google.com/workspace/add-ons/alternate-runtimes-quickstart
* https://developers.google.com/workspace/add-ons/teams-addon-sample
* https://cloud.google.com/functions/docs/deploying/
* https://github.com/GoogleCloudPlatform/functions-framework-python

### September 18, 2021
I got the Quickstart on alternate runtimes working. I was trying to move 
all of the stuff in the common section for the drive interface but there
are properties in the common section that are not in the drive, which is 
why it was failing. The page that talks about the properties is [here](https://developers.google.com/apps-script/manifest/addons).

Started creating a methodology page so that step can be easily recreated.

I found [this article ](https://cloud.google.com/iam/docs/granting-changing-revoking-access) 
in reference to service roles.

### September 21, 2021
Continued adding to the methodology page, finished at step 30. 

Found out that in order to run methods of a service I have to end it with calling 
"execute."

I also found [this article](https://stackoverflow.com/questions/46668084/how-do-i-properly-base64-encode-a-mimetext-for-gmail-api#46668827) 
for actually being able to save message as string, rather than bytes.

### September 23, 2021
I fixed an issue that I had where I couldn't send an email with the recipient
being my person email. The reason being there was an extra @-symbol.

### September 24, 2021
I created the whatToDo.md file to keep track of what I want the app to do.

I also learned that App Engine provides a 5GB default storage. The info
for that can be found [here](https://cloud.google.com/appengine/docs/standard/python3/using-cloud-storage).

I have learned that I did not set up my app engine application and therefore
I may need to add new steps to my project.

### September 30, 2021
I learned that I did not need to use app engine and that all I needed 
to do to store tokens was to save them in a database. This is where 
I discovered Google Datastore as a database. 

### October 5, 2021
For the past few days I was working on a way to store tokens. I figured it out by
using Google Datastore. However I am not sure if this is best way to do so, 
becasue the token is stored in plain text. 

As of now, I am able to click on an item in the Google Drive and an email is 
sent.

### October 12, 2021
Today is my Talk #1 and the previous week I just worked on the slides for this 
project.

After my talk these were the comments made by those in the audience (students and 
teachers):
* GCP Pub/Sub for watching for events
* deletion of a file if there are errors
* logs for when events happen in a text file
* maybe local counterpart 
  * To watch to see if the file is downloaded from the local directory 
  * to let users know if it’s on the machine
* look into Dropbox instead of Google Drive

Then after that discussion I talked with my committee chair, Dr. Chappell, and this
is what he said:
* Mention target audience
* stop only reading the slides
  * Slides should have minimal information which allows you to have more 
  information
* Be clear on whether the add on is running on browser or not 
  * Because we need to know if it needs to be open and running on the machine 
  (do we as the developer have a choice?). 
  * If it’s running on the server how is that handled? 
* Aim the app as if it will be handled by a lot of people
  * Which will influence things like billing
* I’m am aiming this as offering something Zapier doesn’t 
* How do you know when the file is downloaded? 
* It’s important to know if the file is deleted
* Logs for the app is a good idea
  * like to have logs for 
    * start of check
    * end of check
    * events triggered
* Prioritize downloading because if you need to transition to another app, 
you’d have time to do so
* Start presentation with a use case “I’m a podcaster…” 
* Comprehensive exam is in April (first Saturday in April) 
  * It’s offered once a year, so pass it first go.

### October 15, 2021
I decided to look into making a companion app. I found [an article](https://medium.com/analytics-vidhya/how-to-build-your-first-desktop-application-in-python-7568c7d74311)
on creating a desktop application with a GUI.

### October 19, 2021
For about two days I've been trying to figure out the companion app thing. I got a 
basic thing running. 

In an effort to avoid paying for things, I tried to see if I could just connect the Google 
Drive API, which I can but in order to integrate it with Google drive, I'd need to use 
Google Cloud Platform. There is also another issue that the app would be accessible in the 
"create new document" dropdown or the "open with" dropdown which is not the right place for 
the application. Therefore, the Google Worskpace Addon is the right choice if I am to 
continue using Google Drive.

### October 23, 2021
I figured out how to set up the GOOGLE_APPLICATION_CREDENTIALS. I followed [this page](https://cloud.google.com/docs/authentication/getting-started).
Basically I thought that OAuth Client ID was the file the were talking about, but it was actually 
the Service Account Key. I set up this variable in the environment variables field of the
edit configurations page in PyCharm. 

I've been looking into how to monitor changes and I kept getting stuck on [this page] (https://developers.google.com/drive/api/v3/push)
and all it did was tell me that in order to track changes I needed to use the notification 
service which sends notifications to a domain that you own. This was a problem because I 
didn't sign up for a domain and doing so would cost money. 

However, then I looked up "track changes with google drive python" and I found this ["Google Drive
for deveopers article"](https://developers.google.com/drive/api/v3/manage-changes#python) (!!!!) 
This article showed me how to do it via python.

### October 25, 2021
What I have found out today is that a Google API update might bring some major changes. An issue 
I was facing was using v3 of the Google Drive API and getting an empty list of changes. However,
when I ran the API explorer I got a huge list of changes. Turns out, I was using v3 in the code 
but was looking at v2 of the API explorer. Turns out, the page token is described as the token 
used to track future changes, which means that the list of changes you get are all the changes
that occur after the page token. V3 of the Google Drive API requires the page token, v2 doesn't. 
This means that you can get all the changes on a file in v2 and unless you have all page tokens for 
the list, you can only get the future changes using v3. 

### November 9, 2021
I found these two articles to help with the linking issue:
* https://developers.google.com/workspace/add-ons/guides/alternate-runtimes#java_1
  * I noticed that in the example widgets schema, in the openAs attribute of the openLink section of OnClick, that it was set
  to "FULL_SIZE" this gave me the idea that this is how I open up a pop-up
* https://developers.google.com/apps-script/reference/card-service/open-as
  * Told me how to open up a pop up by setting openAs to "OVERLAY"

Found this article to create a bunch of list items from a string to json: https://www.tutorialspoint.com/How-to-convert-string-to-JSON-using-Python
I found this article to help me with knowing all the card attributes: https://developers.google.com/workspace/add-ons/reference/rpc/google.apps.card.v1#google.apps.card.v1.Card

### February 27, 2022
I am going back and collecting the articles that I've used to help me containerize the app:
* https://codelabs.developers.google.com/codelabs/workspace-add-on-nodejs-cloudrun#3 (to introduce me to the use of 
  Cloud Run with Google Workspace addons)
* https://www.jhanley.com/google-cloud-run-getting-started-with-python-and-flask/ (to help me translate the Node.js code
  into Python)
* https://stackoverflow.com/questions/51395936/how-to-get-flask-app-running-with-gunicorn (to help me change the code from being in a 
  development environment to use in a production environment)
* https://codelabs.developers.google.com/codelabs/cloud-run-hello-python3/#3 (to help me change the code from being in a 
  development environment to use in a production environment)
* 