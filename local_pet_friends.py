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
   # Переходим на страницу авторизации
   pytest.driver.get('http://petfriends1.herokuapp.com/login')

   yield

   pytest.driver.quit()


def test_show_my_pets():
   # Вводим email
   pytest.driver.find_element_by_id('email').send_keys('vasya@mail.com')
   # Вводим пароль
   pytest.driver.find_element_by_id('pass').send_keys('12345')
   # Нажимаем на кнопку входа в аккаунт
   pytest.driver.find_element_by_css_selector('button[type="submit"]').click()
   # Проверяем, что мы оказались на главной странице пользователя
   assert pytest.driver.find_element_by_tag_name('h1').text == "PetFriends"