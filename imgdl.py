from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from sys import platform

#Proof of concept flickr downloader using selenium webdriver. (pip install selenium)
#This assumes that the download link will be available which is not always the case.
#Should be further extended and automated to be able to dynamically take photo ids and download them.


#Set chromedriver path. Use exe if windows, binary if linux
driverPath = "./chromedriver.exe"
if platform.startswith('linux'):
    driverPath = "./chromedriver"
	

browser = webdriver.Chrome(executable_path=driverPath) #Set the browser to use. 

print "Loading page"
browser.get('https://flickr.com/photo.gne?id=2177060015') #Navigate to the page by using the link that accepts only photo ids.

newurl = browser.current_url #Get the new url. Navigating to the link above will ultimately resolve the url to its 'proper' url.
newurl = newurl +"/sizes/l" #Append the url with the link to the large (l) download page.
browser.get(newurl) #Navigate there.

downloadText = "Download the Large 1024 size of this photo" #This is the text on the download link.

browser.find_element_by_link_text(downloadText).click() #Click the link. Unless otherwise configured, chrome will save 
                                                        #this link automatically into the downloads folder.

#Todo close the browser with browser.quit(). Doing so here quits the browser before the download is complete.
