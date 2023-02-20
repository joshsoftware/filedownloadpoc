from os import getenv

from time import sleep, time
# from datetime import datetime

import requests
# from selenium import webdriver
from seleniumwire import webdriver  # Import from seleniumwire
from seleniumwire.utils import decode

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains

user_email = getenv("USR_EMAIL")
user_password = getenv("USR_PWD")

browser = webdriver.Firefox() # PhantomJS()
wait = WebDriverWait(browser, 60)
# browser.set_window_size(1024, 768)

def download_audit_trail_from_druva():
    browser.get("https://insync-sagarg.drtst.in")
    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, 'email'))
    )
    email_input.send_keys("c@c.com")
    email_input.send_keys(Keys.RETURN)
    password_input = wait.until(
        EC.presence_of_element_located((By.NAME, 'password'))
    )
    password_input.send_keys("c")
    password_input.send_keys(Keys.RETURN)
    sleep(9)
    cookie = None
    for req in browser.requests:
        res = req.response
        if res and "sagarg" in req.url and not any(req.url.endswith(text) for text in ["js", "css", "html", "ttf"]):
            # print(req.url)
            # print(res.status_code)
            # print(req.headers)
            # print(res.headers)

            # body = decode(res.body, res.headers.get('Content-Encoding', 'identity'))
            # print(body)
            _cookie = req.headers.get('Cookie')
            if _cookie:
                cookie = _cookie
                print(req.url)
                print(cookie)

    payload = {
        "selectedType": "All",
        "selectedInterval": 7,
        "filetype": "csv",
        "activity_subtype": "",
        "user": "",
    }
    r = requests.get("https://insync-sagarg.drtst.in/admin/useractivities/download", params=payload, headers={
        "Cookie": cookie
    })
    # print(r.url)
    # print(r.text)
    # filename = 'files/%s.csv' % datetime.now()
    filename = 'files/%.0f.csv' % time()
    with open(filename, 'w') as f:
        f.write(r.text)

    ## browser.get("https://insync-sagarg.drtst.in/admin/insync/#op=audits-manage")

    # download_btn = wait.until(
    #     EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[6]/div[2]/div/div[3]/div[2]/div/div/div[1]/div/div[1]/div[1]/div[5]/div/div/ul/li/ul/li[2]/a'))
    # )
    # download_btn.click()
    ## download_btn = wait.until(
    ##     EC.presence_of_element_located((By.ID, 'download-useractivities-dropdown'))
    ## )
    # print(download_btn.text)
    # print(dir(download_btn))
    # print("1")
    # elem = download_btn.find_element(By.CLASS_NAME, 'childMenu')
    # print(elem)
    # print(dir(elem))
    # print("2")
    # li = elem.find_element(By.CLASS_NAME, 'item2')
    # a = elem.find_element(By.TAG_NAME, 'a')
    # ActionChains(browser).click(a).perform()
    ## actions = ActionChains(browser)
    ## actions.move_to_element(download_btn).perform()
    ## elem = download_btn.find_element(By.CLASS_NAME, 'childMenu')
    # print(elem.text)
    # actions.move_to_element(elem).perform()
    ## li = elem.find_element(By.CLASS_NAME, 'item2')
    ## a = browser.find_element(By.LINK_TEXT, "Download CSV")
    # a = li.find_element(By.TAG_NAME, 'a')
    # print(a)
    # print(a.get_attribute('href'))
    # print(li.text)
    # a.click()
    # actions.move_to_element(a).perform().click().build().perform()
    ## browser.execute_script("arguments[0].click();", a)

def get_otp_from_email():
    browser.get("https://mail.google.com")

    # email_input = wait.until(
    #     EC.presence_of_element_located((By.ID, 'identifierId'))
    # )
    email_input = wait.until(
        EC.presence_of_element_located((By.NAME, 'identifier'))
    )
    email_input.send_keys(user_email)
    email_input.send_keys(Keys.RETURN)
    sleep(3)
    password_input = wait.until(
        EC.presence_of_element_located((By.NAME, 'Passwd'))
    )
    password_input.send_keys(user_password)
    password_input.send_keys(Keys.RETURN)
    sleep(45)
    print("Searching search input")
    search_input = wait.until(
        EC.presence_of_element_located((By.NAME, 'q'))
    )
    search_input.send_keys("from:%s subject:My OTP" % user_email)
    search_input.send_keys(Keys.RETURN)
    first_email_xpath = "/html/body/div[7]/div[3]/div/div[2]/div[5]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div[6]/div[1]"
    first_email = wait.until(
        EC.presence_of_element_located((By.XPATH, first_email_xpath))
    )
    print(first_email)
    # first_email.click()
    browser.execute_script("arguments[0].click();", first_email)

    first_email_message_body_xpath = "/html/body/div[7]/div[3]/div/div[2]/div[5]/div/div/div/div/div[2]/div/div[1]/div/div[3]/div[6]/div[3]/div/div/div/table/tr/td/div[2]"
    first_email_message_body = wait.until(
        EC.presence_of_element_located((By.XPATH, first_email_message_body_xpath))
    )
    print(first_email_message_body)
    print(first_email_message_body.text)

try:
    # original_window = browser.current_window_handle
    # w = browser.switch_to.new_window()
    # driver.switch_to_window(original_window)
    # download_audit_trail_from_druva()
    get_otp_from_email()
    # browser.switch_to.window(original_window)

except Exception as ex:
    print(ex)
    print("Something went wrong")
finally:
    print("Done")
    sleep(10)
    browser.quit()

