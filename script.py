# pytest -v --driver Chrome --driver-path /path/to//chromedriver.exe
# pytest -v --driver Chrome --driver-path Selenium_testing/webdriver/chrome/chromedriver.exe
# pytest -v --driver Chrome --driver-path C:\chromesetup\chromedriver.exe
# Chrome(executable_path='/webdriver/chrome/chromedriver')

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# options for repl vm running:
chrome_options = Options()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')


def test_search_example():
  driver = webdriver.Chrome(options=chrome_options)
  driver.set_window_size(800, 600)
  driver.maximize_window()
  driver.get("https://google.com")

  time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

  # Find the field for search text input:
  search_input = driver.find_element_by_name('q')


  # Enter the text for search:
  search_input.clear()
  search_input.send_keys('first test')

  time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

  # Click Search:
  search_button = driver.find_element_by_name('btnK')
  search_button.submit()

  time.sleep(1)  # just for demo purposes, do NOT repeat it on real projects!

  # Make the screenshot of browser window:
  driver.save_screenshot('result.png')
