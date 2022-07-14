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

        self.driver = webdriver.Chrome(executable_path='chromedriver_win32\chromedriver.exe', chrome_options=chromeOptions)
        self.driver.get("https://instagram.com/")
        sleep(2)

        # Enter user name
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[1]/div/label/input"
            ).send_keys(username)

        # Enter password
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[2]/div/label/input"
            ).send_keys(pw)

        # Click on Login button
        self.driver.find_element_by_xpath(
            "/html/body/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[3]"
            ).click()

        sleep(3)
        
    
    def getUnfollowers(self, userId):

        try:
            #Navigate to profile and followers
            self.driver.get(f"https://www.instagram.com/{userId}/")
        except Exception as e:
            print(f"Username or Password are incorrect: {e}")

        sleep(5)

        # Number of followers
        numFollowers = int(self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a/div/span").text.replace(",","")) 

        print("Total number of followers: ", numFollowers)

        # Click on followers
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[2]/a").click()
        sleep(5)

        # To scroll till last in the follower box. If followers count is quite high and 
        # your net is slow then increase the sleep(N)
        followersBox  = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[2]")
        
        for i in range(int(numFollowers/3)): 
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followersBox)
            sleep(2)
            print("Extracting friends %",round((i/(numFollowers/3)*100),2),"from","%100")

        # Get all the followers
        fList  = self.driver.find_elements_by_xpath("//div[@class='_aano']//li")        
        
        # Get the user names of all the followers
        followersList = []
        for ele in fList:
            txt = ele.text
            followersList.append(txt.split("\n")[0])

        print("All the followers: ", followersList)
        print("Number of followers extracted: ", len(followersList))
        print("Followers count ended")

        # Close followers box
        self.driver.find_elements_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[1]/div/div[3]/div/button")[0].click()
        sleep(1)

        # Number of following
        numFollowing = int(self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a/div/span").text.replace(",","")) 
        print("Total number of people you follow: ", numFollowing)

        # Click on following
        self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/div/header/section/ul/li[3]/a").click()
        sleep(5)

        # To scroll till last in the following box. If followers count is quite high and 
        # your net is slow then increase the sleep(N)
        followingBox  = self.driver.find_element_by_xpath("/html/body/div[1]/div/div[1]/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div/div/div/div[3]")
        for i in range(int(numFollowing/3)): 
            self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', followingBox)
            sleep(2)
            print("Extracting friends %",round((i/(numFollowing/3)*100),2),"from","%100")

        # Get the all the followers
        fList  = self.driver.find_elements_by_xpath("//div[@class='_aano']//li")
        
        # Get the user names of all the followers
        followingList = []
        for ele in fList:
            txt = ele.text
            followingList.append(txt.split("\n")[0])

        print("All the People you follow: ", followingList)
        print("Number of people you follow extracted: ", len(followingList))
        print("Following count ended")

        # Get the accounts who you doesn't follow back
        unFollowingList = []
        for account in followingList:
            if account not in followersList:
                unFollowingList.append(account)

        print("Number of people who dont follow back: ", len(unFollowingList))
        print("People who don't follow back: ", unFollowingList)

        fileName = userId.replace(".","")

        with open(f"{fileName}.txt", "w") as out:
            out.write(f"Number of accounts who follows you: {len(followersList)}\n")
            out.write(f"Number of accounts you are following: {len(followingList)}\n")
            out.write(f"Number of accounts who doesn't follow back: {len(unFollowingList)}\n\n")
            out.write("Following are the accounts who doesnt follow you back:\n")
            out.write(str(unFollowingList))

        # Save as JSON the unfolllowed list to remove later
        with open(f"{fileName}.json", "w") as out:
            simplejson.dump({"unfollowed": unFollowingList}, out)


    def close(self):
        # Close the driver
        self.driver.quit()


if __name__ == "__main__":
    credentialsPath = "credentials.yml"
    uIdList = ["booksntrekks"]

    with open(credentialsPath, "r") as yamlFile:
        cred = yaml.safe_load(yamlFile)
        id = cred["ID"]
        password = cred["Password"]

    # Login
    myBot = InstaBot(id, password)

    for uid in uIdList:
        start = time()
        print(f"This is the current id: {uid}")
        myBot.getUnfollowers(uid)
        end = time()
        print(f"Time taken for {uid}: {round(end-start, 2)} seconds") 
        print("-----------------------------------------------------------------------\n")

    # Close
    myBot.close()  
