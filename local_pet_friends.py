import time
import pytest
from selenium import webdriver

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
    pytest.driver = webdriver.Chrome('./webdriver/chrome/chromedriver.exe')
    pytest.driver.maximize_window()
    # Переходим на страницу авторизации
    pytest.driver.get('http://petfriends1.herokuapp.com/login')

    yield

    pytest.driver.quit()


def test_show_my_pets():
    # Вводим email
    pytest.driver.find_element_by_id('email').send_keys('test123@yandex.ru')
    # Вводим пароль
    pytest.driver.find_element_by_id('pass').send_keys('123456')
    # Нажимаем на кнопку входа в аккаунт
    pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
    # Проверяем, что мы оказались на главной странице пользователя
    assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"
    # Переходим на страницу /my_pets
    pytest.driver.find_element_by_xpath('//li/a[@href="/my_pets"]').click()
    # Проверка тайтла страницы /my_pets
    assert pytest.driver.title == "PetFriends: My Pets"

    # сбор значений проверяемых элементов
    images = pytest.driver.find_elements_by_css_selector("tbody tr th")
    names = pytest.driver.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[1]")
    breeds = pytest.driver.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[2]")
    ages = pytest.driver.find_elements_by_xpath("//div[@id='all_my_pets']/table/tbody/tr/td[3]")
    descriptions = pytest.driver.find_elements_by_css_selector('.card-deck .card-img-top')

    for i in range(len(names)):
        assert images[i].get_attribute('src') != ''
        assert names[i].text != ''
        assert breeds[i].text != ''
        assert ages[i].text != ''
        # assert descriptions[i].text != ''
        # assert ', ' in descriptions[i]
        # parts = descriptions[i].text.split(", ")
        # assert len(parts[0]) > 0
        # assert len(parts[1]) > 0
