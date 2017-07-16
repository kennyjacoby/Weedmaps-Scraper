import time
from bs4 import BeautifulSoup
from selenium import webdriver

NEIGHBORHOODS = {
	"Poway/Mira Mesa":"north-inland", 
	"Clairemont Kearny":"mesa", 
	"El Cajon":"el-cajon", 
	"Lemon Grove/Spring Valley":"south-east-san-diego", 
	"La Mesa":"east-san-diego", 
	"Mission Valley":"central-san-diego-clubs", 
	"Ocean Beach":"ocean-beach",
	"Pacific Beach":"pacific-beach",
	"Gaslamp District":"central-san-diego",
	"Vista":"vista",
	"Escondido/San Marcos":"north-county",
	"Oceanside":"oceansidecarlsbad",
	"Encinitas":"north-san-diego",
	"La Jolla":"la-jolla",
	"National City/Chula Vista":"south-bay-sd",
	"Ramon/Julian":"ramona-julian",
	"Imperial Beach/Otay Mesa":"imperial-beach-otay-mesa",
	"Normal Heights/North Park":"normal-heights-north-park"
}
F = open("deliveries.txt", "a")

class ScrapingBrowser(webdriver.Chrome):
	def __init__(self, addr, *args, **kwargs):
		super(ScrapingBrowser, self).__init__(*args, **kwargs)
		self.implicitly_wait(6)
		self.get(addr)

	def button_click(self, location):
		self.find_element_by_xpath(location).click()

def scrape(browser, neighborhood, date_of_search):
	browser = getDeliveries(browser)
	soup = BeautifulSoup(browser.page_source, "html.parser")
	listings = soup.findAll("wm-listing-peek", {"listing":"listing"})
	for listing in listings:
		details = listing.find("div", {"class":"details"})
		name = details.find("h1", {"class":"name"}).contents[0].encode('utf8')
		address = details.find("div", {"class":"address"}).contents[0].encode('utf8').upper()
		record = "{}|{}|{}|{}\n".format(name, neighborhood, address, date_of_search)
		F.write(record)
		print(record)
	browser.close()
	
def getDeliveries(browser):
	browser.button_click('//*[@id="multi-map-listing-type-filter"]')
	time.sleep(1)
	soup = BeautifulSoup(browser.page_source, "html.parser")
	dropdown = soup.find("ul", {"class":"dropdown"}).findAll("li")
	for i in range(1, 4):
		if dropdown[i-1].find("input", {"class":"ng-pristine ng-untouched ng-valid ng-not-empty"}) is None:
			if i == 2:
				browser.button_click('/html/body/ion-nav-view/ion-side-menus/ion-side-menu-content/ion-nav-view/ion-view/wm-listings-map/div/wm-multi-map-overlay/div/wm-multi-map-filters/div/div[1]/ul/li[{}]/a'.format(i))
				time.sleep(1)
		else:
			if (i == 1 or i == 3):
				browser.button_click('/html/body/ion-nav-view/ion-side-menus/ion-side-menu-content/ion-nav-view/ion-view/wm-listings-map/div/wm-multi-map-overlay/div/wm-multi-map-filters/div/div[1]/ul/li[{}]/a'.format(i))
				time.sleep(1)
	browser.button_click('//*[@id="multi-map-listing-type-filter"]')
	time.sleep(1)
	return browser

def main():
	start_time = time.time()
	today = time.strftime("%m-%d-%Y")
	for neighborhood in NEIGHBORHOODS:
		url = 'https://weedmaps.com/deliveries/in/' + NEIGHBORHOODS[neighborhood]
		browser = ScrapingBrowser(url)
		scrape(browser, neighborhood, today)
	print('\n{} minutes, {} seconds'.format(int(round((time.time() - start_time)//60)), int(round((time.time() - start_time)%60))))

if __name__ == "__main__":
    main()