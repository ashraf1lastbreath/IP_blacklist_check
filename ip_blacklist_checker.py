import time
import json
import re
# import HTML
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


def get_page(url, driver, vpn_ip):
    """Tell the browser to get a page"""
    print "Please wait, checking IP "+vpn_ip+" for any blacklist ..."
    driver.get(url)
    # print "Sleeping for 20..."
    time.sleep(20)
    return driver
    # return driver

def generate_report(page, vpn_ip):
    """Parse the webage to generate detailled report"""
    print "Genarating Report for IP  ",vpn_ip
    print""
    print "RESULTS FOR  IP  "+vpn_ip+ " : "
    print "-------------------------------------------------"
    result = page.find_element_by_xpath('/html/body/div[4]/div[1]/div[3]/b')    #find first element
    print result.text
    print ""
    no_of_blocklists = re.findall('in(.*?)DNS',str(result.text))         #extract string between delimiters
    no_of_blocklists = re.sub("[^0-9]", "",str(no_of_blocklists) )  #remove non numeric characters  
    if int(no_of_blocklists) > 0:
        print "Create Fail Report"
        result_data = generate_html_fail_report(page, vpn_ip)
        return result_data

    else :
        print "IP not blocked on any DNS servers"
    print ""

   

def generate_html_fail_report(page, vpn_ip):
    table_data  =[]
    result_list =[]
    table_data.append(result_list)
    # result_list.append('VPN Server IP',            'Blocked by  DNS Server')

    print "Generating HTML Fail Report for IP  "+vpn_ip
   
    print "Ip " + vpn_ip+" is blacklisted on following DNS Servers :"
    # blocklist = page.find_elements_by_xpath('//*[@id="red_bg_td"]')      #find all elements
    blocklist = page.find_elements_by_xpath('//*[@id="red_bg_td"]/a')
    for block in blocklist:
        print block.text
        result_list = [vpn_ip, "               ",block.text]
        table_data.append(result_list)

    # print "table_data :",table_data
    return table_data


def parse_url(url, vpn_ip):
    """Calling function which calls all other fucntions to parse html"""
    driver, display = start_driver()
    page = get_page(url, driver, vpn_ip)
    result_data = generate_report(page, vpn_ip)
    return result_data
    close_driver(driver, display)


if __name__ == '__main__':
    final_result=[]
    base_url = "https://www.whoisthisip.com/ipblock/"
    json_data =  json.loads(open('VPN_ip.json').read())
    for vpn_ip in json_data["vpn_server_ip"]:
        url = base_url+vpn_ip
        print ""
        print "Checking DNS Blocklist for VPN Server Ip : ",vpn_ip
        print "======================================================================"
        result_data = parse_url(url, vpn_ip)
        final_result.append(result_data)

        f = open ('results.txt','w')
        f.write("VPN Server IP            Blocked by  DNS Server")
        for result in final_result:
            for dns in result:
                for servers in dns :
                    #print dns
                    f.write(str(dns)+'\n')
        f.close()
