# coding=UTF-8

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from delayed_assert import expect, assert_expectations
import time


@pytest.fixture(autouse=True)
def testing():
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--window-size=1280,800")
    driver = webdriver.Chrome('./webdriver/chrome/chromedriver.exe', options=chrome_options)
    driver.implicitly_wait(10)
    # go to auth page
    driver.get('http://petfriends1.herokuapp.com/login')

    yield driver

    driver.quit()


def test_show_my_pets(testing):
    # add email
    testing.find_element_by_id('email').send_keys('test123@yandex.ru')
    # add password
    testing.find_element_by_id('pass').send_keys('123456')
    # click submit button
    testing.find_element_by_css_selector('button[type="submit"]').click()
    # user main page check
    assert testing.find_element_by_tag_name('h1').text == "PetFriends"
    # go to /my_pets
    testing.find_element_by_xpath('//li/a[@href="/my_pets"]').click()
    # /my_pets-title check
    assert testing.title == "PetFriends: My Pets"
    title = testing.find_element_by_css_selector('head title')
    assert title.get_attribute("innerText") == "PetFriends: My Pets"

    # сбор значений проверяемых элементов
    pet_number = len(testing.find_elements_by_css_selector("table.table-hover tbody > tr"))
    images = testing.find_elements_by_css_selector("tbody tr th img")
    names = testing.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[1]")
    breeds = testing.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[2]")
    ages = testing.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[3]")

    images_counter = 0
    names_set = set()
    pets_list = set()
    for i in range(pet_number):
        
        names_set.add(names[i].text)
        pet = (names[i].text, breeds[i].text, ages[i].text)
        pets_list.add(pet)
        
        if images[i].get_attribute('src') != '':
            images_counter +=1
        expect(images[i].get_attribute('src') != '', 'Pet has no picture')
        expect(names[i].text != '', 'Empty name field')
        expect(breeds[i].text != '', 'Empty name field')
        expect(ages[i].text != '', 'Empty age field')

    # all pets are displayed on the page
    pet_number_stat = testing.find_elements_by_xpath("/html/body/div[1]//div[@class='.col-sm-4 left']")
    expect((int(pet_number_stat[0].text.split("\n")[1].split(" ")[1])) == pet_number, 'Not all pets are displayed on '
                                                                                      'the page')

    # More then a half of pets has photo number
    expect(images_counter >= pet_number / 2, 'Less then a half of pets has photo number')

    # all pets has different names
    expect(len(names) == len(names_set), 'Match of pet names')

    # all pets has different set of name, breed and age
    expect(pet_number == len(pets_list), 'Not all of pets has different set of name, breed and age')

    assert_expectations()



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