import yaml
from time import sleep
from selenium import webdriver


class InstaBot:
    def __init__(self, username, pw):

        self.username = username
        self.password = pw

        chromeOptions = webdriver.ChromeOptions()
        chromeOptions.add_argument("--incognito")

        # Replace 'ChromeDriverPath' with chrome driver's path in your local
        self.driver = webdriver.Chrome(executable_path='ChromeDriverPath', chrome_options=chromeOptions)
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
        
    
    def getUnfollowers(self, userId):

        try:
            #Navigate to profile and followers
            self.driver.get(f"https://www.instagram.com/{userId}/")
        except Exception as e:
            print(f"Username or Password are incorrect: {e}")

        # Click on followers
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        sleep(5)

        # Number of followers
        numFollowers = int(self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[2]/a/span").text.replace(",","")) 

        # TO scroll till last in the follower box
        followersBox  = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        for i in range(int(numFollowers/2)): 
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followersBox)
            sleep(1)
            print("Extracting friends %",round((i/(numFollowers/2)*100),2),"from","%100")

        # Get all the followers
        fList  = self.driver.find_elements_by_xpath("//div[@class='PZuss']//li")
        
        # Get the user names of all the followers
        followersList = []
        for ele in fList:
            txt = ele.text
            followersList.append(txt.split("\n")[0])

        print("Followers count ended")

        # Close followers box
        self.driver.find_elements_by_xpath("/html/body/div[4]/div/div/div[1]/div/div[2]/button")[0].click()
        sleep(1)


        # Click on following
        self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a").click()
        sleep(5)

        # Number of following
        numFollowing = int(self.driver.find_element_by_xpath("/html/body/div[1]/section/main/div/header/section/ul/li[3]/a/span").text.replace(",","")) 

        # TO scroll till last in the following box
        followingBox  = self.driver.find_element_by_xpath("/html/body/div[4]/div/div/div[2]")
        for i in range(int(numFollowing/2)): 
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followingBox)
            sleep(1)
            print("Extracting friends %",round((i/(numFollowing/2)*100),2),"from","%100")

        # Get all the following
        fList  = self.driver.find_elements_by_xpath("//div[@class='PZuss']//li")
        
        # Get the user names of all the follwoing accounts
        followingList = []
        for ele in fList:
            txt = ele.text
            followingList.append(txt.split("\n")[0])

        print("Following count ended")

        # Get the accounts who you doesn't follow back
        unFollowingList = []
        for account in followingList:
            if account not in followersList:
                unFollowingList.append(account)

        fileName = userId.replace(".","")

        with open(fileName, "w") as out:
            out.write(f"Number of accounts who follows you: {len(followersList)}\n")
            out.write(f"Number of accounts you are following: {len(followingList)}\n")
            out.write(f"Number of accounts who doesn't follow back {len(unFollowingList)}\n")
            out.write("Following are the accounts who doesnt follow you back:\n")
            out.write(str(unFollowingList))


    def close(self):
        # Close the driver
        self.driver.quit()


credentialsPath = "yamlFilePath.yml"

with open(credentialsPath, "r") as yamlFile:
    cred = yaml.safe_load(yamlFile)

    id = cred["ID"]
    password = cred["Password"]


# Login
myBot = InstaBot(id, password)

# Mention the usernames of accounts you want to check for unfollowers.
# Note: Followers of the mentioned accounts should be accessible from the 
# account mentioned in credentials.yml
uIdList = ["usernames1", "usernames2", "usernames3", "usernames4"]

for uid in uIdList:
    print(f"This is the current id: {uid}")
    myBot.getUnfollowers(uid) 
    print("------------------------------------------------------")
    print()

# Close
myBot.close()  

