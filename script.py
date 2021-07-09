# pytest -v --driver Chrome --driver-path /path/to//chromedriver.exe

# pytest -v --driver Chrome --driver-path /webdriver/chrome/chromedriver.exe

# pytest -v --driver Chrome --driver-path C:\chromesetup\chromedriver.exe

# #Simple assignment
# from selenium.webdriver import Chrome

# driver = Chrome()

# #Or use the context manager
# from selenium.webdriver import Chrome

# with Chrome() as driver:
#     #your code inside this indent

# Chrome(executable_path='/webdriver/chrome/chromedriver')

# import selenium
# from selenium import webdriver

# driver = webdriver.Chrome() #получение объекта веб-драйвера для нужного браузера

# selenium.get('https://google.com')

# selenium.quit()