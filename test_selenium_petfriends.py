from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# options for repl vm running:
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def test_petfriends():
  driver = webdriver.Chrome(options=chrome_options)
  driver.maximize_window()
  driver.get("https://petfriends1.herokuapp.com/")

  time.sleep(3)  # just for demo purposes, do NOT repeat it on real projects!

  # click on the new user button
  btn_newuser = driver.find_element_by_xpath("//button[@onclick=\"document.location='/new_user';\"]")
  btn_newuser.click()
    
  # click existing user button
  btn_exist_acc = driver.find_element_by_link_text(u"У меня уже есть аккаунт")
  btn_exist_acc.click()

  # add email
  field_email = driver.find_element_by_id("email")
  field_email.clear()
  field_email.send_keys("<your_email>")
    
  # add password
  field_pass = driver.find_element_by_id("pass")
  field_pass.clear()
  field_pass.send_keys("<your_password>")
    
  # click submit button
  btn_submit = driver.find_element_by_xpath("//button[@type='submit']")
  btn_submit.click()

  time.sleep(5)  # just for demo purposes, do NOT repeat it on real projects!
  if driver.current_url == 'https://petfriends1.herokuapp.com/all_pets':
    driver.save_screenshot('result_petfriends.png')
    
  else:
    raise Exception("login error")
