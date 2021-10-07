# Methodology 
**Date: August 24th 2021**  
**Author: Tailon Russell**

## Step 1
Create a project. From the Google Cloud Platform dashboard click the project 
dropdown.

![Alt text](media/selectingProjectDropdown.png)
If there was no project already created then a new one would be created by 
going to [this page](https://console.cloud.google.com/cloud-resource-manager).

## Step 2
Then select "New Project" on the top right of the popup

![Alt text](media/newProjectButton.png)
If on the other page select "Create Project" next to the "Manage Resources"
text.

## Step 3
Set the project name*. Then click the create button.

![Alt text](media/projectName.png)
*The project ID can be edited by selecting "EDIT" next to the project ID

Make sure before continuing that the selected project is the one that was 
just created, which can be done by selecting the project dropdown, and 
selecting the new project. 

## Step 4
Select "Go To APIs Overview" in the dashboard on the Homepage*. 

![Alt text](media/apiSection.png)
*If not on the Homepage, select "Google Cloud Platform" on the banner.

## Step 5
Select "Enable APIs and Services"

![Alt text](media/enableAPIs.png)

## Step 6 
Search for Gmail API, click "Gmail API" from the results, and click the 
"Enable" button.

![Alt text](media/welcomeAPIPage.png)
![Alt text](media/gmailSearchResults.png)
![Alt text](media/enableAPIButton.png)

Repeat for the Google Drive API.

## Step 7
On the APIs Overview page, selection "Credentials" from the sidebar and
then select "Configure the Consent Screen." The consent screen the screen 
that appears that asks if a user wants to authorize an app. 

![Alt text](media/credentialsPage.png)

## Step 8
The button directs to the OAuth consent screen. Here the app is user type
of the app must be selected. Select "Internal" and once the app is ready
to be published the type must be set to "External." Then click the "create"
button.

![Alt text](media/userType.png)

## Step 9
Next fill out the app registration form and select "Save and Continue."
Since no logo and domain has been created, the "app domain" section was
left blank, as well as the "authorized domains" section. 

![Alt text](media/appRegistration.png)

After this page will be the "scopes" page of the app registration
process. The scopes can be left blank, as they will be added in the
deploymen.json file. Therefore, just click "save and continue"

The final page is "summary" from there just click "back to dashboard."

## Step 10
Go back to "credentials page," select "Create credentials" and click
"OAuth client ID"

![Alt text](media/createClientId.png)

## Step 11 
Then select "Desktop App" from the application type drop down list,
set the Client ID name, and click the "create button."

![Alt text](media/clientIDName.png)

## Step 12
In the popup that appears, click the "Download JSON" button.

![Alt text](media/downloadJSON.png)

The downloaded file needs to be renamed "credentials" and included
in the working directory of the project.

## Step 13
Select the hamburger menu on the left side of the banner, hover
over "IAM & Admin", and select "Service Accounts"

![Alt text](media/selectServiceAccount.png)

## Step 14
On the service accounts page, select "Create Service Account."

![Alt text](media/serviceAccountPage.png)

## Step 15
Fill out the service account details and then select "Create and 
Continue." The service account description is left blank because 
what the service account will do is unclear. 

![Alt text](media/createServiceAccount.png)

## Step 16 
Grant the service account access to project, set this to owner.
Grant users access to this service account, add the desired email
address(s). Then select "Done"

## Step 17 
Select the service account.

![Alt text](media/serviceAccount.png)

## Step 18
Next select the "Keys" tab, click the "Add Key" button, and select
"Create New Key" from the dropdown.

![Alt text](media/createNewKeyServiceAccount.png)

Then select the JSON key type and click "create" on the bottom right.

![Alt text](media/createPrivateKeyServiceAccount.png)

A file storing the private key will be downloaded to the machine.
It is best practice to **not** put the key in the working directory
of a project and to **not** leave it in Downloads folder.

## Step 19 
Select the "Details" tab and click the "Show Domain-Wide Delegation"
dropdown.

![Alt text](media/domainDelegationServiceAccount.png)

Check the box labeled "Enable Google Workspace Domain-Wide Delegation."
Then click the save button. Coppy the 

![Alt text](media/enableDelegationServiceAccount.png)

## Step 20
Create a new PyCharm project. Miniconda was previously installed 
and PyCharm automatically detected the installation and used it
as a Python interpreter. 

Follow the instructions on the [Python Quickstart page](https://developers.google.com/gmail/api/quickstart/python).
(Excluding renaming the file to quickstart.py -- it was left as main.py)

The app was authorized to view emails.

## Step 21
Follow the instructions on the [Quickstart for creating an addon in a different language](https://developers.google.com/workspace/add-ons/alternate-runtimes-quickstart).

First, enable billing. Get to the billing page by clicking on the 
hamburger menu and selecting "Billing."

![Alt text](media/getToBillingPage.png)

Click "link to a billing account" Select a billing account or create a 
billing account. 

## Step 22 
Second, install Cloud SDK. Cloud SDK needs a bundled Python solution 
to link to and since Miniconda is being used for this project,
Cloud SDK needed to link to Miniconda. To do this, the instructions
given in [this Medium article](https://medium.com/swlh/installing-google-cloud-sdk-to-use-python-from-anaconda-94890014e4e8).
(step 1 can be ignored because Python was already installed). Once 
that is done, then PyCharms needs to be restarted. 

## Step 23
Follow the rest of the steps in the [Quickstart for creating an addon in a different language](https://developers.google.com/workspace/add-ons/alternate-runtimes-quickstart).
Enter the command:
> gcloud init

If it's the first time it will ask to pick a project to configure, if 
it's not it'll ask to re-initialize with current settings or to create a
new configuration. 

>Welcome! This command will take you through the configuration of gcloud.  
> Settings from your current configuration [default] are:  
> core:  
> &nbsp; account: XXXXXXXXXXXXXXXXX  
> &nbsp; disable_usage_reporting: xxxx  
> &nbsp; project: XXXXXXXXXX 
>
> Pick configuration to use:  
> &nbsp; [1] Re-initialize this configuration [default] with new settings  
> &nbsp; [2] Create a new configuration  
> Please enter your numeric choice:

After entering "2", set the configuration name. Then set the account that 
will utilize the configuration

Next select whether to configure with a preexisting project or to configure
by creating a new project. 

> Pick cloud project to use:  
> &nbsp; [1] driveaddon-2122  
> &nbsp; [2] gold-pier-324719  
> &nbsp; [3] Create a new project  
> Please enter numeric choice or text value (must exactly match list
item):

After entering "1" the project, Cloud SDK has successfully been logged in
and the project has been configured with Cloud SDK. Enter one of the core
commands listed in the ["Getting Started with Cloud SDK" page](https://cloud.google.com/sdk/docs/quickstart)
to confirm.

## Step 24
Continuing with the [Quickstart for creating an addon in a different language](https://developers.google.com/workspace/add-ons/alternate-runtimes-quickstart),
create a Cloud Function.

Enter the following command to enable Google Cloud Functions, Cloud Build, 
the Add-ons API:
> gcloud services enable cloudfunctions cloudbuild.googleapis.com gsuiteaddons.googleapis.com

## Step 25
Now, since the Quickstart is for JavaScript, the exact code can't be used, 
since this project is written in Python.

According to Google Cloud Guides, for JavaScript to process HTTP requests, 
the function needs to have two parameters, however in Python the function 
only takes one parameter. Also, Python can return JSON object from a list 
that is formatted similar to a diction and using the dumps function of the
JSON package (Note: this is not the only way). 

The file would look like 
> import json
>
> def load_homepage(req):  
> &nbsp;&nbsp;&nbsp;&nbsp;return create_action()
>
> def create_action():  
> &nbsp;&nbsp;&nbsp;&nbsp; cards = {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"action": {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"navigations": [  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;{  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"pushCard": {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"header": {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;"title": "Cats!"  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"sections": [  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;{  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"widgets": [  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;"textParagraph": {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"text": "Your random cat:"  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;}  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;{  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;"image": {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"imageUrl": "https://cataas.com/cat"  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;}  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;}  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;}  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;]  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
> &nbsp;&nbsp;&nbsp;&nbsp;}  
> &nbsp;&nbsp;&nbsp;&nbsp;return json.dumps(cards)

The function names were renamed to fit the Python naming conventions.

## Step 26
Continuing on in the [Quickstart for creating an addon in a different language](https://developers.google.com/workspace/add-ons/alternate-runtimes-quickstart),
The function will be deployed by the following command:
> gcloud functions deploy load_homepage --runtime python39 --trigger-http

Note: The function name next to "deploy" must be the name of a function in the file. 
The runtime is also different from the Quickstart, other supported runtimes can be 
found in [this documentation](https://cloud.google.com/sdk/gcloud/reference/functions/deploy#--runtime).
This runtime is Python 3.9.

A prompt will then appear asking to allow unauthenticated users to invoke the 
function. According to a [Google Cloud article ](https://cloud.google.com/run/docs/authenticating/public) 
on authentication, this should be allowed if the service will be a public API or website.

Enter "y" and the function then deployed. Verifying the function was deployed, the following 
command was entered:
> gcloud functions call load_homepage

The following was the response
>executionId: xxxxxxxxxxxx  
> result: '{"action": {"navigations": [{"pushCard": {"header": {"title": "Cats!"}, "sections":  
> &nbsp; [{"widgets": [{"textParagraph": {"text": "Your random cat:"}}, {"image": {"imageUrl":  
> &nbsp; "https://cataas.com/cat"}}]}]}}]}}'

## Step 27
Next in the [Quickstart for creating an addon in a different language](https://developers.google.com/workspace/add-ons/alternate-runtimes-quickstart)
is to authorize Google to invoke the app.

After entering the commands:
> gcloud workspace-add-ons get-authorization

The name, OAuthClientID, and serviceAccountEmail will be displayed. Copying the 
serviceAccountEmail into the command:
> gcloud functions add-iam-policy-binding load_homepage --role roles/cloudfunctions.invoker --member serviceAccount:**SERVICE_ACCOUNT_EMAIL**

Will authorize Google to invoke the app. Note: replace the text "Service_account_email" with 
the actual service account email. Make sure the name of the function matches the name of the 
deployed function. 

## Step 28
Continuing in the [Quickstart for creating an addon in a different language](https://developers.google.com/workspace/add-ons/alternate-runtimes-quickstart),
the deployment resource needs to be created. Note: there seems to multiple names for this. 
The two other names for this are "manifest" and "addon interface," and "addon" could be swapped
for any google app such as drive, gmail, sheets, etc. There doesn't seem to be a reason
for the distinction.

Next, the deployment.json file was created.

> deployment.json  
> 
> {  
> &nbsp;&nbsp;&nbsp;&nbsp;"oauthScopes": ["https://www.googleapis.com/auth/drive.addons.metadata.readonly"],  
> &nbsp;&nbsp;&nbsp;&nbsp;"addOns": {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"common": {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"name": "My HTTP Add-on",  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"logoUrl": "https://github.com/webdog/octicons-png/raw/master/black/beaker.png",  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"homepageTrigger": {  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
> &nbsp;&nbsp;&nbsp;&nbsp;"runFunction": "https://us-central1-driveaddon-2122.cloudfunctions.net/load_homepage"  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;}  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;},  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"gmail": {},  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"drive": {},  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"calendar": {},  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"docs": {},  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"sheets": {},  
> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"slides": {}  
> &nbsp;&nbsp;&nbsp;&nbsp;}  
>}  

Since the project is a drive addon, the OAuth scopes needed to be changed for a drive specific
scope. In order to get the url for the function so that "runFunction" would work, the following
command had to be run:
> gcloud functions describe load_homepage

The url listed under httpsTrigger once the command ran had to be copied and pasted into the 
"runFunction" field.

Note: The Quickstart uses "https://www.googleapis.com/auth/gmail.addons.execute" for the 
OauthScopes, however this does not seem to exist anymore (A list of OAuth scopes can be
found [here](https://developers.google.com/identity/protocols/oauth2/scopes)).

## Step 29
Next in the [Quickstart for creating an addon in a different language](https://developers.google.com/workspace/add-ons/alternate-runtimes-quickstart),
the following command needed to be ran:
> gcloud workspace-add-ons deployments create driveaddon --deployment-file=deployment.json

Note: "driveaddon" could be any name, and the file name assigned to the deploymen-file flag
needs to the name of the deployment resource file. 

This creates the deployment. 

Next the deployment needs to be deployed, which was achieved by running the following 
command:
> gcloud workspace-add-ons deployments install driveaddon

Then refresh the Google Drive of the Google account linked to the Google Cloud Platform 
project. The app will show up on the right side panel.

![Alt text](media/appLocation.png)

Notice that the icon does not appear, this is because the link to the icon (what was 
assigned to iconUrl in the deployment resource) is broken, so a different link was 
assigned and the following command was ran to update the deployment.
> gcloud workspace-add-ons deployments replace driveaddon --deployment-file=deployment.json

Then Google Drive was refreshed and the new icon appears. 

This replaces the deployment with another. This is being used as a way to update the 
deployment, but there is a command to directly update the deployment by running the command:
> gcloud deployment-manager deployments update driveaddon
 
Note: If it's the first time running command a prompt will ask to enable the deployment-manager.

## Step 30

When you click on the icon another side panel will open on the right. Since it's the first
time clicking the icon, the side panel will display a blurb and an option to authorize the app.

![Alt text](media/appSidePanel.png)

Once the "authorize access" link is clicked a pop up will appear to accept the app to have
access to certain aspects of the user's Google Drive account. What the app will request 
access for is determined by OAuth Scopes list in the deployment resource file.

## Step 31
Moving on to incorporating the use of the Gmail API, the "main" function was renamed to 
be "authenticate," the section in the code that accesses the Gmail API was deleted, and 
the function just returns the credentials. The function looks thusly:
> def authenticate():  
>&nbsp;&nbsp;&nbsp;&nbsp;scopes = [   
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"https://www.googleapis.com/auth/gmail.addons.current.action.compose",
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"https://www.googleapis.com/auth/gmail.send", 
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;"https://www.googleapis.com/auth/gmail.compose",
>"https://www.googleapis.com/auth/datastore" 
> &nbsp;&nbsp;&nbsp;&nbsp;]  
>&nbsp;&nbsp;&nbsp;&nbsp;creds = None  
>&nbsp;&nbsp;&nbsp;&nbsp;client = datastore.Client("driveaddon-2122")  
>&nbsp;&nbsp;&nbsp;&nbsp;token = get_most_recent_token(client)  
>&nbsp;&nbsp;&nbsp;&nbsp;creds = Credentials.from_authorized_user_info(token, scopes)  
>&nbsp;&nbsp;&nbsp;&nbsp;# If there are no (valid) credentials available, let the user log in.  
>&nbsp;&nbsp;&nbsp;&nbsp;if not creds or not creds.valid:  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;if creds and creds.expired and creds.refresh_token:  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;creds.refresh(Request())  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;client = datastore.Client("driveaddon-2122", credentials=creds)  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;store_token(client, creds)  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;else:  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;flow = InstalledAppFlow.from_client_secrets_file('credentials.json', scopes)  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;creds = flow.run_local_server(port=0)  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;# Save the credentials for the next run  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;client = datastore.Client("driveaddon-2122", credentials=creds)  
>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;store_token(client, creds)  
>&nbsp;&nbsp;&nbsp;&nbsp;return creds

This function stores the tokens in Google Datastore which was access using the datastore api.
This was necessary so that previously created tokens (that are still valid) could be accessed. The previous
method of storing the token in a file was not working correctly.

## Step 32
Once the token was able to be accessed, then an email was able to be sent.
The respond_to_trigger function looked like below:
>def respond_to_trigger(req):  
>&nbsp;&nbsp;&nbsp;&nbsp;creds = authenticate()  
>&nbsp;&nbsp;&nbsp;&nbsp;service = create_service('gmail', 'v1', creds)  
>&nbsp;&nbsp;&nbsp;&nbsp;user_info = service.users().getProfile(userId='me').execute()  
>&nbsp;&nbsp;&nbsp;&nbsp;the_sender = user_info["emailAddress"]  
>&nbsp;&nbsp;&nbsp;&nbsp;the_recipient = "tailrusse2020@gmail.com"  
>&nbsp;&nbsp;&nbsp;&nbsp;the_subject = "testing again again and again"  
>&nbsp;&nbsp;&nbsp;&nbsp;the_text = "You should see this when I select a file"  
>&nbsp;&nbsp;&nbsp;&nbsp;the_message = create_message(the_sender, the_recipient, the_subject, the_text)  
>&nbsp;&nbsp;&nbsp;&nbsp;send_message(service, "me", the_message)  
>&nbsp;&nbsp;&nbsp;&nbsp;request_json = req.get_json(silent=True)  
>&nbsp;&nbsp;&nbsp;&nbsp;selected_itmes = request_json["drive"]["selectedItems"]  
>&nbsp;&nbsp;&nbsp;&nbsp;first_item = selected_itmes[0]  
>&nbsp;&nbsp;&nbsp;&nbsp;return create_card(first_item["title"], first_item["iconUrl"])  

## Step 33
While this was valuable in order to learn more about the Google API, it is not 
the functionality that is desired for this app as currently, when the item is 
clicked an email is sent. 