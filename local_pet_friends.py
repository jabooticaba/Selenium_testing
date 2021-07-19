# coding=UTF-8

import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_petfriends(web_browser):
    web_browser.get("https://petfriends1.herokuapp.com/")

    # click on the new user button
    btn_newuser = web_browser.find_element_by_xpath("//button[@onclick=\"document.location='/new_user';\"]")
    btn_newuser.click()

    # click existing user button
    btn_exist_acc = web_browser.find_element_by_link_text(u"У меня уже есть аккаунт")
    btn_exist_acc.click()

    # add email
    field_email = web_browser.find_element_by_id("email")
    field_email.clear()
    field_email.send_keys("<your_email>")

    # add password
    field_pass = web_browser.find_element_by_id("pass")
    field_pass.clear()
    field_pass.send_keys("<your_password>")

    # click submit button
    btn_submit = web_browser.find_element_by_xpath("//button[@type='submit']")
    btn_submit.click()

    # time.sleep(4)  # just for demo purposes, do NOT repeat it on real projects!
    assert web_browser.current_url == 'https://petfriends1.herokuapp.com/all_pets',"login error"


@pytest.fixture(autouse=True)
def testing():
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--window-size=1280,800")
    pytest.driver = webdriver.Chrome('./webdriver/chrome/chromedriver.exe', options=chrome_options)

    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield

    pytest.driver.quit()

def test_show_my_pets():
    # add email
    pytest.driver.find_element_by_id('email').send_keys('test123@yandex.ru')
    # add password
    pytest.driver.find_element_by_id('pass').send_keys('123456')
    # click submit button
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # Переходим на страницу /my_pets
    pytest.driver.find_element_by_xpath('//li/a[@href="/my_pets"]').click()
    # Проверка тайтла страницы /my_pets
    assert pytest.driver.title == "PetFriends: My Pets"
    title = pytest.driver.find_element_by_css_selector('head title')
    assert title.get_attribute("innerText") == "PetFriends: My Pets"

    # сбор значений проверяемых элементов
    pet_number = len(pytest.driver.find_elements_by_css_selector("table.table-hover tbody > tr"))
    images = pytest.driver.find_elements_by_css_selector("tbody tr th img")
    names = pytest.driver.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[1]")
    breeds = pytest.driver.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[2]")
    ages = pytest.driver.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[3]")

    images_counter = 0
    names_set = set()
    pets_list = set()
    for i in range(pet_number):
        
        names_set.add(names[i].text)
        pet = (names[i].text, breeds[i].text, ages[i].text)
        pets_list.add(pet)
        
        if images[i].get_attribute('src') != '':
            images_counter +=1
        # assert images[i].get_attribute('src') != '' #TODO Need to add soft assert
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''

        
    
    
#     images_counter = 0
#     names_set = set()
#     pets_list = []
#     for i in range(pet_number):
#         pet = []
#         pet.append(names[i].text), pet.append(breeds[i].text), pet.append(ages[i].text)

#         names_set.add(names[i].text)
#         if images[i].get_attribute('src') != '':
#             images_counter +=1
#         # assert images[i].get_attribute('src') != '' #TODO Need to add soft assert
#         assert names[i].text != ''
#         assert breeds[i].text != ''
#         assert ages[i].text != ''

#         if pet not in pets_list:
#             pets_list.append(pet)

    # assertion of pet number in statistics frame and number of pet cards
    pet_number_stat = pytest.driver.find_elements_by_xpath("/html/body/div[1]//div[@class='.col-sm-4 left']")
    assert (int(pet_number_stat[0].text.split("\n")[1].split(" ")[1])) == pet_number

    # More then a half of pets has photo number
    assert images_counter >= pet_number / 2

    # all pets has different names
    assert len(names) == len(names_set)

    # all pets are different
    assert pet_number == len(pets_list)

