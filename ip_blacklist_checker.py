import time
from selenium import webdriver
from pyvirtualdisplay import Display

def start_driver():
    """Open headless chromedriver"""
    print 'Starting Web driver...'
    display = Display(visible=0, size=(800, 600))
    display.start()
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome('/root/IP_blacklist_check/chromedriver', chrome_options=chrome_options)
    #driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chrome.exe")
    # print "Sleeping for 4 ..."
    time.sleep(4)
    return driver, display

def close_driver(driver, display):
    """Close chromedriver"""
    print "Closing Web driver..."
    display.stop()
    driver.quit()
    print "Chrome driver closed successfully. "


def get_page(url, driver):
    """Tell the browser to get a page"""
    print "Please wait, getting your webpage ..."
    driver.get(url)
    # print "Sleeping for 20..."
    time.sleep(20)
    return driver
    # return driver

def generate_report(page):
    """Parse the webage to generate detailled report"""
    print "Genarating Report for your IP ... "
    print""
    print "RESULTS FOR YOUR IP : "
    print "======================================================================"
    result = page.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/b')    #find first element
    print result.text
    print ""
    print "Your Ip is blacklisted on following DNS Servers :"
    print "-------------------------------------------------"
    blocklist = page.find_elements_by_xpath('//*[@id="red_bg_td"]')      #find all elements
    for block in blocklist:
        print block.text
    print ""


def parse_url(url):
    """Calling function which calls all other fucntions to parse html"""
    driver, display = start_driver()
    page = get_page(url, driver)
    generate_report(page)
    close_driver(driver, display)


if __name__ == '__main__':
    url = "https://www.whoisthisip.com/ipblock"
    parse_url(url)
