from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.expected_conditions import presence_of_element_located, presence_of_all_elements_located
import platform
import traceback
import time


class InstagramBot():
    def __init__(self, username, password):
        if platform.system() == "Windows":
            driverSelect = './driver/chromedriver.exe'
        else:
            driverSelect = './driver/chromedriver'

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--start-maximized")
        chromeOptions.add_experimental_option(
            "prefs", {"intl.accept_languages": "en,en_US"})

        self.browser = webdriver.Chrome(
            executable_path=driverSelect, options=chromeOptions)
        self.browserWait = WebDriverWait(self.browser, 10)
        self.username = username
        self.password = password

    def signIn(self):
        self.browser.get("https://www.instagram.com/accounts/login/")

        input = self.browserWait.until(
            presence_of_all_elements_located((By.CLASS_NAME, "_2hvTZ")))

        usernameInput = input[0]
        passwordInput = input[1]

        usernameInput.send_keys(self.username)
        passwordInput.send_keys(self.password)
        passwordInput.send_keys(Keys.ENTER)

        time.sleep(2)

        return True

    def followWithUsername(self, username):
        self.browser.get("https://www.instagram.com/{}/".format(username))
        time.sleep(2)

        followButton = self.browserWait.until(
            presence_of_all_elements_located((By.CLASS_NAME, "_5f5mN")))[0]

        if followButton.text != "Following":
            followButton.click()
            time.sleep(2)

            print("Success following {}".format(username))
        else:
            print("You're already following {}".format(username))

    def unfollowWithUsername(self, username):
        self.browser.get("https://www.instagram.com/{}/".format(username))
        time.sleep(2)

        followButton = self.browserWait.until(
            presence_of_all_elements_located((By.CLASS_NAME, "_5f5mN")))[0]

        if followButton.text == "Following":
            followButton.click()
            time.sleep(2)

            confirmationButton = self.browserWait.until(
                presence_of_element_located((By.CLASS_NAME, '-Cab_')))
            confirmationButton.click()

            print("Success unfollow {}".format(username))
        else:
            print("You're not following {}".format(username))

    def followFormTag(self, tag, max, interval):
        self.browser.get('https://www.instagram.com/explore/tags/' + tag)
        postList = self.browser.find_elements_by_class_name("v1Nh3")
        numberOfPostInList = len(postList)

        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfPostInList < max):
            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfPostInList = len(
                self.browser.find_elements_by_class_name("v1Nh3"))
            print(numberOfPostInList)

        for post in self.browser.find_elements_by_class_name("v1Nh3"):
            post.click()

            followButton = self.browserWait.until(
                presence_of_element_located((By.CLASS_NAME, "oW_lN")))
            username = self.browserWait.until(
                presence_of_element_located((By.CLASS_NAME, "FPmhX")))
            if followButton.text != "Following":
                followButton.click()

                print("Success following {}".format(
                    username.get_attribute("title")))

                time.sleep(interval)
            else:
                print("You're already following {}".format(
                    username.get_attribute("title")))

            closeButton = self.browserWait.until(
                presence_of_all_elements_located((By.CLASS_NAME, "wpO6b")))
            closeButton[-1].click()
            time.sleep(2)

    def followFromAutoherUser(self, username, max, interval):
        self.browser.get('https://www.instagram.com/' + username)
        followersLink = self.browser.find_element_by_css_selector('ul li a')
        followersLink.click()
        time.sleep(2)
        followersList = self.browser.find_element_by_css_selector(
            'div[role=\'dialog\'] ul')
        numberOfFollowersInList = len(
            followersList.find_elements_by_css_selector('li'))

        followersList.click()
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOfFollowersInList < max):
            actionChain.key_down(Keys.CONTROL).click(
                followersList).key_up(Keys.CONTROL).perform()

            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOfFollowersInList = len(
                followersList.find_elements_by_css_selector('li'))
            print(numberOfFollowersInList)

        followers = []
        for user in followersList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector(
                'a').get_attribute('href')
            username = user.find_element_by_css_selector('a').text

            try:
                followButton = user.find_element_by_xpath("div/div[3]/button")

                if followButton.text != "Following":
                    followButton.click()

                    print("Success following {}".format(username))
                else:
                    print("You're already following {}".format(username))

                time.sleep(interval)
            except Exception as identifier:
                pass

            followers.append(userLink)

            if (len(followers) == max):
                break

        return followers

    def unfollowFromFollowing(self, max, interval):
        self.browser.get(
            'https://www.instagram.com/{}/following/'.format(self.username))
        followingsLink = self.browser.find_elements_by_class_name('-nal3')[-1]
        followingsLink.click()
        time.sleep(2)
        followingsList = self.browser.find_element_by_css_selector(
            'div[role=\'dialog\'] ul')
        numberOffollowingsInList = len(
            followingsList.find_elements_by_css_selector('li'))

        followingsList.click()
        actionChain = webdriver.ActionChains(self.browser)
        while (numberOffollowingsInList < max):
            actionChain.key_down(Keys.CONTROL).click(
                followingsList).key_up(Keys.CONTROL).perform()

            actionChain.key_down(Keys.SPACE).key_up(Keys.SPACE).perform()
            numberOffollowingsInList = len(
                followingsList.find_elements_by_css_selector('li'))
            print(numberOffollowingsInList)

        followings = []
        for user in followingsList.find_elements_by_css_selector('li'):
            userLink = user.find_element_by_css_selector(
                'a').get_attribute('href')
            username = user.find_element_by_css_selector('a').text

            try:
                unfollowButton = user.find_element_by_xpath(
                    "div/div[2]/button")

                if unfollowButton.text == "Following":
                    unfollowButton.click()

                    confirmationButton = self.browserWait.until(
                        presence_of_element_located((By.CLASS_NAME, '-Cab_')))
                    confirmationButton.click()

                    print("Success unfollowing {}".format(username))
                else:
                    print("You're already unfollowing {}".format(username))

                time.sleep(interval)
            except Exception as identifier:
                pass

            followings.append(userLink)

            if (len(followings) == max):
                break

        return followings

    def closeBrowser(self):
        self.browser.close()

    def askOptions(self):
        print("\n\n")
        print("-------------------------------------------------------------------")
        print("Kamu mau ngapain pake aplikasi ini? inget ya kalo dibanned saya gak tanggung jawab")
        print("Kalo gitu pilih angka sesuai kamu mau ngapain")
        print("1. Follow pengguna sesuai username")
        print("2. Unfollow pengguna sesuai username")
        print("3. Follow user dari kompetitor mu")
        print("4. Follow user dari postingan dengan hastag tertentu")
        print("5. Unfollow user dari daftar following")
        print("6. Udahan ah males mau pake aplikasi ini")

        option = int(input("Kamu pilih yang mana? : "))

        if option == 1:
            username = input("Masukin username nya : ")

            print("Tunggu ya lagi proses...")

            self.followWithUsername(username)

            return self.askOptions()
        elif option == 2:
            username = input("Masukin username nya : ")

            print("Tunggu ya lagi proses...")

            self.unfollowWithUsername(username)

            return self.askOptions()
        elif option == 3:
            print("Gunakan interval yang manusiawi")
            username = input("Masukin username nya : ")
            max = int(input("Maksimal berapa orang yang mau kamu follow? : "))
            interval = int(input("Masukkan interval follow (dalam detik) : "))

            print("Tunggu ya lagi proses...")

            self.followFromAutoherUser(username, max, interval)

            return self.askOptions()
        elif option == 4:
            print("Gunakan interval yang manusiawi")
            tag = input("Masukin tag nya : ")
            max = int(input("Maksimal berapa post yang mau kamu lihat? : "))
            interval = int(input("Masukkan interval follow (dalam detik) : "))

            print("Tunggu ya lagi proses...")

            self.followFormTag(tag, max, interval)

            return self.askOptions()
        elif option == 5:
            print("Gunakan interval yang manusiawi")
            max = int(input("Maksimal berapa orang yang mau kamu unfollow? : "))
            interval = int(input("Masukkan interval follow (dalam detik) : "))

            print("Tunggu ya lagi proses...", )

            self.unfollowFromFollowing(max, interval)

            return self.askOptions()
        elif option == 6:
            return self.closeBrowser()
        else:
            print("=========================================")
            print("Milih yang bener dong, sesuain nomernya")
            print("=========================================\n")
            return self.askOptions()

    def __exit__(self, exc_type, exc_value, traceback):
        self.closeBrowser()


if __name__ == "__main__":
    print("Halo! Ini adalah instagram bot untuk auto follow dan unfollow, gunakan dengan bijak. \nApabila kamu dibanned oleh pihak instagram saya selaku kreator dari bot ini tidak bertanggung jawab")

    username = input("Masukkan username mu : ")
    password = input("Masukkan password mu : ")

    bot = InstagramBot(username, password)

    print("Tunggu beberapa saat, sedang proses login")

    if (bot.signIn()):
        print("=======================")
        print("Login telah berhasil...")
        print("=======================")

        bot.askOptions()
    else:
        print("Ada yang salah dengan username dan password yang dimasukkan")
        bot.closeBrowser()

    # bot.followWithUsername("gogarmen")
    # bot.unfollowWithUsername("gogarmen")
    # bot.followFromAutoherUser("gogarmen", 10)
    # bot.followFormTag("sablon", 40)
