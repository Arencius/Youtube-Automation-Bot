# Youtube automation bot that adds songs from your favorite artists to the playlist for you. 

## IMPORTANT
1) Bot is built with Opera Webdriver, so if you'd like to use it with different browser, you need to download right driver (e.g. chromedriver if you use Chrome) suitable for your browser version, and add it to PATH. Operadriver.exe is already included in the repository.
2) Browsers launched with selenium have weird "security systems". It means that there could be problems with signing into your YouTube account. If that problem occurs, please turn off two-step verification, or allow your account to launch less secure applications. After you've done that, you should be able to log in correctly.
3) To sign in properly, you need to provide your (correct) mail and password in secrets.py file.


## ABOUT PROJECT AND HOW IT WORKS 
After launching the project, chosen browser will open on YouTube main page (www.youtube.com). Then you'll be asked to provide artists you want the Bot to search for (in video title and descriptions) and name of playlist in which the videos will be saved. Having done that, the bot will automatically sign into your youtube account with data provided in secrets.py file. Selenium browsers are not perfect, so after succesful login you may be redirected either to main youtube page or studio.youtube.com (what happened in my case). Then you need to paste the link of whatever song you wish in the browser and that's basically everything you had to do. Since now, the bot checks if song belongs to artists you provided in the second step and if so, adds songs to the playlist.
