import pytest
import uuid
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from os import name as os_name


@pytest.fixture
def driver_args():
    return ['--log-level=3']


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep


@pytest.fixture()
def testing(request):
    chrome_options = Options()
    chrome_options.headless = True
    chrome_options.add_argument("--window-size=1280,800")
    if os_name == 'posix':
        driver = webdriver.Chrome('./webdriver/chrome/chromedriver', options=chrome_options)
    else:
        driver = webdriver.Chrome('./webdriver/chrome/chromedriver.exe', options=chrome_options)

    driver.implicitly_wait(10)
    # go to auth page
    driver.get('http://petfriends1.herokuapp.com/login')

    yield driver

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            file_name = str(uuid.uuid4())
            driver.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            driver.save_screenshot('screenshots/' + file_name + '.png')

            # For happy debugging:
            log_to_file = []

            print('URL: ', driver.current_url)
            print('Browser logs:')
            for log in driver.get_log('browser'):
                print(log)
                log_to_file.append(log)

            # Save browser logs and page source code to file
            with open('logs/' + file_name + '.txt', 'w') as txt_file:
                txt_file.write('Browser logs:' + str(log_to_file))
                txt_file.write("\n" + "----------------------------- Page sourse -------------------------------" + "\n" + "\n")
                txt_file.write(driver.page_source)

        except:
            pass  # just ignore any errors here

    driver.quit()
