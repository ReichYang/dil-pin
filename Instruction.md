# Instructions for the Pinterest Image Retrieval & Analysis Platform 
This web application used an official Pinterest API to retrieve the data about the user and the images. Also, we provided functions to obtain some basic image properties and to analyze the images.

##Login Page
First of all, you have to log in using your Pinterest email, username, and password. All of them have to correct to pass the Pinterest authentication. If you fail to log in (the page refreshes itself time after time), please refer to the error messages on the top of the screen. 

## Search Page
### View and download user information
On the left of the screen, you can see all the information about your account. These are the information Pinterest stored on their server. If you press the “Download My Info” button, it will automatically return a .json file that contains all of the information shown on the left screen.
### Search Images
On the top of the page, you can input search queries into the search box, and then click the “Search” button. We now set the number of pictures returned as 150, and all the retrieved pictures will be displayed on the right part of the screen. 
### View Images Description
To see the description of the images, just hover on the images with your cursor. The descriptions will be shown right after you put your mouse on that specific image.
### View Images Metadata & Metadata Search
To zoom in and see the larger version of the image, just click on the image thumbnail. The larger version of the image will pop up below the search bar. Also, these attributes of this image will be displayed consequently:
-	Dominant Color 
-	Color Palette
-	Created Time
-	Grid Title
-	Is Promoted
-	Is Uploaded

There is more metadata associated with each pin, to search the specific metadata, just type in any letter in the search box under the “Pin Info” and it will show you any metadata attributes start with this letter. For example, if you want to see the board linked with this pin, just type in b, and select “board”. Finally, press Enter to let the new attributes showed in the panel as a new entry. **You have to press enter to activate the attribute addition.**
![alt text](https://github.com/ReichYang/dil-pin/blob/master/search.png "Search Example")


### Download Images to the Server
After you search for any terms, you can download the images to the server. Just click the button called “Download Pictures to the Server”, and it will automatically download all the returned images. The number of the pictures downloaded will show on the button after all the downloads have finished.
### Redirect to the Image Analysis Page
Click the “Go to the Image Analysis Page” buttons on either the left or the right of the screen.

## Analysis Page
### Upload Google Vision Key (Underdevelopment)
You can upload your Google Vision key so the web application could run object detections on your specified images. Click the “Upload Key” button and select your key ending with .json. Once you select the file to upload, the file name will appear below the button. **You have to press the “Submit” button so that the key file could be uploaded to the server.** The result of the upload, such as success or failure, will show consequently after the page is refreshed.
### View Images in the Folder
You can view all the pictures downloaded from Pinterest. To do this, select the folder you want to peek in on the selection bar on the left of the screen, and then click “Peek in This Folder”. All the pictures in this folder will be displayed at the bottom of the page, along with a tag indicating the number of the pictures in this folder.
### Download Images to Your Local Working Station
To download the pictures on the server, just click on the button with the text “Download This Folder to Your Local PC”. The downloading will be processed in right after and a zip file containing all the pictures in your specified folder will be returned.
### Image Analysis
Our web application can show you some summary statistics about the images in a folder. To do so, simply click on the “Analyze This Folder” button, and the results will be shown on the right of the screen. It only takes 15 pictures of the selected folder to analyze. Remember to select the folder, you have to make sure the folder is focused and its label turns blue. For now, the supported analysis includes:
-	Description Wordcloud
-	Domain Wordcloud
-	Board Wordcloud
-	Promoter Wordcloud
-	Date Graph
### Download Analysis Results
The analysis plots and their crude text data can be download to your local working station as well. Click the light green button on the right of the screen and all the associated analysis files and plots will be zipped up and downloaded in a second.
