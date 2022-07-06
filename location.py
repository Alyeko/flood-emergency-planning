from selenium import webdriver 
from selenium.webdriver.chrome.options import Options 
from selenium.webdriver.support.ui import WebDriverWait
import time
from pyproj import Transformer

def get_user_coords():  #this code was adapted from https://codeburst.io/how-i-understood-getting-accurate-geolocation-using-python-web-scraping-and-selenium-7967d721587a
    print('For optimal results, make sure your mobile data is on and wifi off, ...')
    options = Options()
    options.add_argument("--use--fake-ui-for-media-stream")
    driver = webdriver.Chrome(executable_path = './chromedriver.exe',options=options) #Edit path of chromedriver accordingly
    timeout = 20
    driver.get("https://mycurrentlocation.net/")
    wait = WebDriverWait(driver, timeout)
    time.sleep(3)
    longitude = driver.find_elements_by_xpath('//*[@id="longitude"]')
    longitude = [x.text for x in longitude]
    longitude = str(longitude[0])
    
    latitude = driver.find_elements_by_xpath('//*[@id="latitude"]')
    latitude = [x.text for x in latitude]
    latitude = str(latitude[0])
    driver.quit()
    
    transformer = Transformer.from_crs(4326, 27700)
    return transformer.transform(latitude, longitude)  #covert lat, long to osgb36 coords
