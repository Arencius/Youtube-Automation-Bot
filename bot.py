from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import NoSuchElementException 
from secrets import GOOGLE_EMAIL, PASSWORD
from time import sleep


class YoutubeBot:
    def __init__(self,artists, playlist_name, private = True, redirect_url = 'https://www.youtube.com'):
        """ 
        Youtube Bot class constructor.

        :param artists: Artists whose songs will be added to the playlist.
        :param playlist_name: Name of the playlist to add songs to.
        :param private: boolean type, determines playlist accessibility (if hadn't existed).
        :param redirect_url: Link to redirect after succesful login. Optionally the main YT page.
        """
        self.driver = webdriver.Opera()                     # change driver if you use different browser
        self.driver.get('https://www.youtube.com')
        self.url = self.driver.current_url
        self.artists_to_search = artists
        self.playlist_name = playlist_name
        self.playlist_private = private

        try:
            self.youtube_login()
            self.driver.get(redirect_url)
        except Exception:
            pass
        

    def run(self):
        """ Main function, refreshes the page every second to check if played song has been changed. """
        while True:
            sleep(1)    # checking if URL has changed (new song is played)
            if self.url != self.driver.current_url:
                self.url = self.driver.current_url
                sleep(1)
                if self.song_matches():
                    self.add_to_playlist()


    def youtube_login(self):
        """ Automates proccess of logging into youtube account using data provided in secrets.py file. """

        login_button = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="action-button"]')))
        login_button.click()

        # entry for google e-mail
        login_entry = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'div.Xb9hP > input')))
        login_entry.send_keys(GOOGLE_EMAIL)

        # confirm mail button
        ok_login = self.driver.find_element_by_id('identifierNext')
        ok_login.click()

        # entry for google account password
        password_entry = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="password"]/div[1]/div/div[1]/input')))
        password_entry.send_keys(PASSWORD)

        # confirm password button
        ok_password = self.driver.find_element_by_id('passwordNext')
        ok_password.click()

    def song_matches(self):
        '''Checks if currently played song belongs to given author, 
        based on video title and description. 
        
        :return: bool
        '''

        video_title = self.driver.find_element_by_css_selector('h1.title.style-scope.ytd-video-primary-info-renderer').text.lower()
        video_description = WebDriverWait(self.driver,1).until(EC.presence_of_element_located((By.XPATH, "//*[@id='description']/yt-formatted-string"))).text.lower()
        
        artists_in_title, artists_in_description = False, False
        for artist in self.artists_to_search:
            if artist in video_title:
                artists_in_title = True
            if artist in video_description:
                artists_in_description = True

        return (artists_in_title or artists_in_description)

    def add_to_playlist(self):
        """ If song matches the requirements, function adds it to the playlist. """
        
        playlist_button = WebDriverWait(self.driver, 3).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="top-level-buttons"]/ytd-button-renderer[2]')))
        playlist_button.click()  # opens popup with playlists
 
        sleep(1)

        playlists = WebDriverWait(self.driver,2).until(EC.presence_of_all_elements_located((By.XPATH, "//div[@id='playlists']/ytd-playlist-add-to-option-renderer/paper-checkbox/div[@id = 'checkboxLabel']/div/div[@id='checkbox-label']/yt-formatted-string[@id='label']")))
        playlist_titles = [p.text for p in playlists]   # extracting titles from webelements

        if self.playlist_name in playlist_titles:    # if playlist exists
            # index of specified playlist in the list
            index = playlist_titles.index(self.playlist_name)

            xpath = f"//div[@id='playlists']/ytd-playlist-add-to-option-renderer[{index+1}]/paper-checkbox/div[@id ='checkboxContainer']"
            add_button = self.driver.find_element_by_xpath(xpath)

            # child element having a 'checked' class if button is clicked to ensure that song won't be deleted from playlist
            checkbox = self.driver.find_element_by_xpath(f"{xpath}/div[@id='checkbox']")

            # if song is not in the playlist
            if not 'checked' in checkbox.get_attribute('class'):
                add_button.click()
            self.close_window(add_button)
        else:                               # if playlist doesn't exist
            self.create_playlist()

    def close_window(self, element):
        """ Closes popup after succesfully adding a song to playlist.

        :param element: Document Object Model element, on which the action will be performed (closing).       
        """    
        action = ActionChains(self.driver)
        action.move_to_element_with_offset(element, -50, 0)  # moves cursor 50px to the left
        action.click()
        action.perform()

    def create_playlist(self):
        """ Creates new playlist if there hadn't existed playlist with given name. """
        
        new_playlist_button = self.driver.find_element_by_xpath('//*[@id="content-icon"]')
        new_playlist_button.click()

        name_input = self.driver.find_element_by_xpath('//*[@id="input-1"]/input')
        name_input.send_keys(self.playlist_name)

        if self.playlist_private:
            access_label = self.driver.find_element_by_xpath('//*[@id="dropdown-trigger"]')
            access_label.click()

            private_icon = WebDriverWait(self.driver,1).until(EC.element_to_be_clickable((By.XPATH, '//ytd-privacy-dropdown-item-renderer[3]/paper-item')))
            private_icon.click()

        submit_button = self.driver.find_element_by_xpath('//*[@id="actions"]/ytd-button-renderer')
        submit_button.click()
