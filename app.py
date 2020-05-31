from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from secrets import GOOGLE_EMAIL, PASSWORD
from time import sleep


class YoutubeBot:
    def __init__(self):
        self.driver = webdriver.Opera()  # change driver if you use different browser
        self.driver.get('https://www.youtube.com')
        self.url = self.driver.current_url

        self.artists_to_search, self.playlist_name = self.get_data()
        self.youtube_login()

        sleep(20)  # thread waits with another actions for user to change the URL
        while True:
            # checking if URL has changed (new song is played)
            sleep(1)
            if self.url != self.driver.current_url:
                self.url = self.driver.current_url
                sleep(1)
                if self.song_matches():
                    self.add_to_playlist()

    def get_data(self):
        '''Function executed right after loading the YouTube window and before 
        logging into account. User provides name of the artist and playlist in which
        given artist's song should be saved.'''

        artists = input(
            'Artist/s to be searched (separated by comma): ').split(',')
        playlist = input(
            "Playlist name (will be created if doesn't exist): ")
        print('Logging in...')
        return (artists, playlist)

    def youtube_login(self):
        '''Automates proccess of logging into youtube account using data provided in secrets.py file.
        After succesful signing in, user has to manually play a song. '''

        # css selector of 'SIGN IN' button on the main youtube page
        sign_in_button = '#buttons.ytd-masthead > *.ytd-masthead'
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, sign_in_button))).click()  # waits with clicking for website to fully load

        # entry for google e-mail
        login_entry = self.driver.find_element_by_css_selector(
            'div.Xb9hP > input')
        login_entry.send_keys(GOOGLE_EMAIL)

        # confirm button
        ok_login = self.driver.find_element_by_id('identifierNext')
        ok_login.click()

        sleep(2)

        # entry for google account password
        password_entry = self.driver.find_element_by_css_selector(
            'input.whsOnd.zHQkBf')
        password_entry.send_keys(PASSWORD)

        # confirm button
        ok_password = self.driver.find_element_by_id('passwordNext')
        ok_password.click()

    def song_matches(self):
        '''Checks if currently played song belongs to given author, 
        based on video title and description. Returns bool.'''

        video_title = self.driver.find_element_by_css_selector(
            'h1.title.style-scope.ytd-video-primary-info-renderer').text.lower()
        video_description = self.driver.find_element_by_xpath(
            "//div[@id='content']/div[@id='description']/yt-formatted-string").text.lower()

        artists_in_title, artists_in_description = False, False
        for artist in self.artists_to_search:
            if artist in video_title:
                artists_in_title = True
            if artist in video_description:
                artists_in_description = True

        return (artists_in_title or artists_in_description)

    def add_to_playlist(self):
        sleep(1)
        playlist_button = self.driver.find_element_by_xpath(
            "//div[@id='top-level-buttons']/ytd-button-renderer[2]")
        playlist_button.click()  # opens popup with playlists

        sleep(1)  # waits so all elements in popup are properly loaded

        playlists = self.driver.find_elements_by_xpath(
            "//div[@id='playlists']/ytd-playlist-add-to-option-renderer/paper-checkbox/div[@id = 'checkboxLabel']/div/div[@id='checkbox-label']/yt-formatted-string[@id='label']")
        # extracting titles from webelements
        playlist_titles = [p.text for p in playlists]

        if self.playlist_name in playlist_titles:    # if playlist exists
            # index of specified playlist in the list
            index = playlist_titles.index(self.playlist_name)

            xpath = f"//div[@id='playlists']/ytd-playlist-add-to-option-renderer[{index+1}]/paper-checkbox/div[@id ='checkboxContainer']"

            add_button = self.driver.find_element_by_xpath(xpath)

            # child element having a 'checked' class if button is clicked to ensure that song won't be deleted from playlist
            checkbox = self.driver.find_element_by_xpath(
                f"{xpath}/div[@id='checkbox']")

            # if song is not in the playlist
            if not 'checked' in checkbox.get_attribute('class'):
                add_button.click()
            self.close_window(add_button)
        else:                               # if playlist doesn't exist
            self.create_playlist()

    def close_window(self, element):
        '''Closes popup after succesfully adding a song to playlist.'''
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(
            element, -50, 0)  # moves cursor 50px to the left
        action.click()
        action.perform()

    def create_playlist(self):
        '''Creates new playlist if there hadn't existed playlist with given name. '''
        new_playlist_button = self.driver.find_element_by_xpath(
            "//div[@id='actions']/ytd-add-to-playlist-create-renderer")
        new_playlist_button.click()

        name_input = self.driver.find_element_by_xpath(
            "//div[@id='labelAndInputContainer']/iron-input/input")
        name_input.send_keys(self.playlist_name)

        submit_button = self.driver.find_element_by_xpath(
            "//div[@id='actions']/ytd-button-renderer/a/paper-button[@id='button']")
        submit_button.click()


if __name__ == '__main__':
    bot = YoutubeBot()
