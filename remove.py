import sys
import yaml
import simplejson
from time import sleep, time
from selenium import webdriver


class InstaBot:
    def __init__(self, username, pw):

        self.username = username
        self.password = pw

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--incognito")

        self.driver = webdriver.Chrome(executable_path='/home/soulreaper/Documents/study/unfollowed/chromedriver', chrome_options=chromeOptions)
        self.driver.get("https://instagram.com/")
        sleep(2)

        # Enter user name
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[2]/div/label/input"
            ).send_keys(username)

        # Enter password
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[3]/div/label/input"
            ).send_keys(pw)

        # Click on Login button
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div/form/div[4]"
            ).click()
        sleep(3)


    def remove(self, userId):
        try:
            #Navigate to profile and followers
            self.driver.get(f"https://www.instagram.com/{userId}/")
        except Exception as e:
            print(f"Username or Password are incorrect: {e}")
            return

        sleep(2)

        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/div/header/section/div[1]/div[2]/span/span[1]/button"
        ).click()
        sleep(1)

        self.driver.find_element_by_xpath(
            "/html/body/div[4]/div/div/div/div[3]/button[1]"
        ).click()
        sleep(1)


    def close(self):
        # Close the driver
        self.driver.quit()


if __name__ == "__main__":

    credentialsPath = sys.argv[1]
    jsonPath = sys.argv[2]

    with open(jsonPath, "r") as file:
        unfollowedDict = simplejson.load(file)
    unfollowedList = unfollowedDict["unfollowed"]

    with open(credentialsPath, "r") as yamlFile:
        cred = yaml.safe_load(yamlFile)
        id = cred["ID"]
        password = cred["Password"]

    myBot = InstaBot(id, password) # Login

    for uid in unfollowedList: # Remove
        print(uid)
        myBot.remove(uid) 

    myBot.close() # Close