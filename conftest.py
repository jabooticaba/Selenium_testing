import pytest
import uuid
import json

@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.binary_location = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
    chrome_options.add_argument('--kiosk')
    chrome_options.headless = True
    return chrome_options


# @pytest.fixture
# def driver_args():
#     return ['--log-level=DEBUG']

@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    # This function helps to detect that some test failed
    # and pass this information to teardown:

    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)
    return rep

@pytest.fixture
def web_browser(request, selenium):

    browser = selenium
    browser.set_window_size(1400, 1000)

    # Return browser instance to test case:
    yield browser

    # Do teardown (this code will be executed after each test):

    if request.node.rep_call.failed:
        # Make the screen-shot if test failed:
        try:
            file_name = str(uuid.uuid4())
            browser.execute_script("document.body.bgColor = 'white';")

            # Make screen-shot for local debug:
            browser.save_screenshot('screenshots/' + file_name + '.png')

            # For happy debugging:
            log_to_file = []

            print('URL: ', browser.current_url)
            print('Browser logs:')
            for log in browser.get_log('browser'):
                print(log)
                log_to_file.append(log)

            # Save browser logs and page source code to file
            with open('logs/' + file_name + '.txt', 'w') as txt_file:
                txt_file.write('Browser logs:' + str(log_to_file))
                txt_file.write("\n" + "----------------------------- Page sourse -------------------------------" + "\n" + "\n")
                txt_file.write(browser.page_source)

        except:
            pass  # just ignore any errors here
