# Master Project Timeline
This is the timeline for the development of the Master project from 
the creation of the idea through the development of the project.

### March 11th, 2021 
Developed the original idea and noted the new ideas 
that Lawlor presented. Then I created the document “Ideas”. 

### August 24th, 2021 
Discussed with CJ Emerson the possibility of using automation for 
content management and deleting old files. Another option 
discussed was working with KSUA in automating the process of 
uploading audio to KSUA and playing it in automation. 

### August 25, 2021 Discussed with Kevin Swenson about working with
KSUA on automating the automation process (uploading audio and 
loading it into zetta). Turns out there is quite a bit of automation 
already. When audio is uploaded to the Recently Uploaded, that audio 
is downloaded into a folder of the same name. Then Gselector looks at 
that file’s metadata and compares it with other files that were 
previously loaded that are associated with the volunteer’s show 
(these are called links). If the metadata is new and it is the most 
recent file in the recently uploaded, then it is uploaded to zetta. 
The only human input is scheduling the show for the right time. This 
is more of a sanity check so that there weren’t any mistakes made. 

Kevin S. also noted that other projects that could be useful to KSUA 
is automatically recording shows. The parameters are to start 
recording at the top of the hour, keep the audio for a month, and 
then delete the file. 

Another idea that Kevin S. talked about was 
creating a “plugin” for Zetta for filling out data for configuring 
files. 

### August 26, 2021 
I first looked [this article](https://www.thepodcasthost.com/planning/automation-systems-set-you-free/) 
for how to automate the podcast workflow. However, I kept thinking 
about the fact that this is all too simple, not easy necessarily, 
but simple. The problem with the idea is that it is around creating 
something that is not technically complex, which at the least, is 
what a Master’s project and thesis is supposed to focus on. 

While thinking about this I came across the topic of automation 
using AI. I first discovered an [IBM article](https://www.ibm.com/cloud/automation) 
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

Then I started learning about the authorization process. I followed [the docs](https://developers.google.com/drive/api/v3/about-auth) 
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

I then found [an article](https://medium.datadriveninvestor.com/simple-text-summarizer-using-nlp-d8aaf5828e68) 
talking about creating a text summarizer using Python. 

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
I searched for how to create a Google Drive plugin and found [this article](https://developers.google.com/workspace/add-ons/how-tos/building-gsuite-addons). 

Other articles found when researching:
 * Google's tips for UX design: https://developers.google.com/workspace/add-ons/guides/gsuite-style
 * Installing Google Cloud SDK for use with Miniconda's python: https://medium.com/swlh/installing-google-cloud-sdk-to-use-python-from-anaconda-94890014e4e8
   * Learned that I had to restart PyCharm to fix the issue described in step 4