from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import ElementNotVisibleException
from sys import platform
import csv

#Proof of concept flickr downloader using selenium webdriver. (pip install selenium)
#This assumes that the download link will be available which is not always the case.
#Should be further extended and automated to be able to dynamically take photo ids and download them.


#Set chromedriver path. Use exe if windows, binary if linux
driverPath = "./chromedriver.exe"
if platform.startswith('linux'):
    driverPath = "./chromedriver"

browser = webdriver.Chrome(executable_path=driverPath) #Set the browser to use. 
print("Loading page")

#--------------------------Read CSV function--------------------------#
def read_csv(path : "csv file path") -> "tuple":
	"""
	before calling this function.
	Make sure the category titles and extra lines at the end of the csv file is removed
	"""
	#dictionary - id : privacy setting
	id_privacy = {}
	#id only
	ids = []

	with open(path) as f:
		reader = csv.reader(f, delimiter = '\t')
		for row in reader:
			id_privacy[row[0]] = row[3]
			ids.append(row[0])
	return ids, id_privacy

#--------------------download_img function-------------------------------#
def download_img(ids : "id list", all = False, n = 99):
	"""
	The default number of images to be downloaded is 100, set all = True to download all of them
	"""

	totalUndownloadable = 0 #Number of images with downloads disabled/unavailable.
	totaldownloaded = 0 # Number of images that are successfully downloaded

	#if user want to download all images
	if all:
		n = len(ids) - 1
	
	#downloading!
	for key in ids[1:n]:
		photoID = key
		browser.get('https://flickr.com/photo.gne?id='+photoID) #Navigate to the page by using the link that accepts only photo ids.

		newurl = browser.current_url #Get the new url. Navigating to the link above will ultimately resolve the url to its 'proper' url.
		newurl = newurl +"/sizes/o" #Append the url with the link to the original size (o) download page.
		browser.get(newurl) #Navigate there.

		downloadText = "Download the Original size of this photo" #This is the text on the download link.

		try:
			browser.find_element_by_link_text(downloadText).click() #Click the link. Unless otherwise configured, chrome will save this link automatically into the downloads folder.
		except:
			print("Cannot download image " + photoID)  #If the browser is unable to find this link, skip this image and document which id was unavailable.
			totalUndownloadable = totalUndownloadable + 1
		else:
			totaldownloaded += 1
	
		#Print statistics regarding undownloadable images.
		print("Total number of images downloaded: " + str(totaldownloaded) + "\t Total number undownloadable images: " + str(totalUndownloadable) + " images. ("+str((totalUndownloadable/99281)*100)+"%)")

#Todo close the browser with browser.quit(). Doing so here quits the browser before the download is complete.



if __name__ == "__main__":
	ids, id_privacy = read_csv("cleaned.csv")
	download_img(ids)
