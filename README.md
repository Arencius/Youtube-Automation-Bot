# Youtube automation bot that adds songs from your favorite artists to the playlist for you. 

## IMPORTANT
1) Bot is built with Opera Webdriver, so if you'd like to use it with different browser, you need to download right driver (e.g. chromedriver if you use Chrome) suitable for your browser version, and add it to PATH. Operadriver.exe is already included in the repository.
2) Browsers launched with selenium have weird "security systems". It means that there could be problems with signing into your YouTube account. If that problem occurs, please turn off two-step verification, or allow your account to launch less secure applications. After you've done that, you should be able to log in correctly.
3) To sign in properly, you need to provide your (correct) mail and password in secrets.py file.


## ABOUT PROJECT AND HOW IT WORKS 
After launching the project, you will see the window, where you are asked to fill all important data, such as: 
- names/nicknames of artists that you want to search for, separated by comma
- link to redirect after closing this window. If you leave this input empty, the main Youtube page will be loaded.
- name of playlist, that you want to store songs in. If the playlist with the given name does not exist, it will be created 
- accesibility of playlist - determines whether the playlist should be public or private. Works only if playlist doesn't already exist (does not modify accesibility of already created playlists)

Having filled all the forms, the bot will automatically log in to your account, and redirect to the provided link/youtube.com. Autoplay is highly recommended to be active, since you won't have to do anything.
