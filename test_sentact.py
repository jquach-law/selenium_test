import time
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager


URL = "https://sentact.com/"
DRIVER_OPTIONS = ['--no-sandbox',
                '--disable-extensions',
                '--incognito',
                '--headless',
                '--disable-gpu']

@pytest.fixture
def driver():
    """
    Description:
    Selenium Chrome driver function set as pytest fixture.
    Fixture driver is passed into test functions and is closed after test completion.

    Args: -
    Returns: -
    """
    # Select driver's options
    chrome_options = webdriver.ChromeOptions()
    for option in DRIVER_OPTIONS:
        chrome_options.add_argument(option)

    # Execute driver
    driver = webdriver.Chrome(service=ChromeService(
        ChromeDriverManager().install()), options=chrome_options)
    
    driver.implicitly_wait(3)
    
    # Navigate/close entire browser
    driver.get(URL)
    yield driver
    driver.quit()


def _bring_element_into_view(driver, xpath):
    """
    Description:
    Scroll to an element on the web page, ensuring it becomes visible.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        xpath (str): The XPath of the element to locate and scroll to.

    Returns:
        WebElement: The located and scrolled-to WebElement.
    """
    # Locate the element
    element = driver.find_element(By.XPATH, xpath)
    
    # Scroll to the element
    driver.execute_script("arguments[0].scrollIntoView();", element)
    
    # Wait for the element to become visible
    WebDriverWait(driver, 3).until(EC.visibility_of(element))
    
    return element


def test_turning_products_carousel(driver):
    """
    Description:
    Asserts SentactRounding's block is hidden after click ther right arrow

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns: -
    """
    # Locate carousel and right arrow by XPATH
    right_arrow = _bring_element_into_view(driver, '//*[@id="content"]/div/div/section[2]/div[3]/div/div/div[3]/div/div/div/div/div[3]')

    # Click right arrow
    ActionChains(driver).move_to_element(right_arrow).click().perform()

    # Find SentactRounding's hidden attribute
    sentact_rounding = driver.find_element(By.XPATH, '//*[@id="content"]/div/div/section[2]/div[3]/div/div/div[3]/div/div/div/div/div[1]/div/div/div[3]')
    aria_hidden = sentact_rounding.get_attribute('aria-hidden')

    assert 'true' == aria_hidden


def test_play_video(driver):
    """
    Description:
    Asserts the center page video plays after clicking the play button

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns: -
    """
    # Locate iframe by XPATH
    iframe = _bring_element_into_view(driver, '//*[@id="content"]/div/div/section[3]/div[2]/div/div/section[1]/div/div[2]/div/div/div/div/iframe')
    
    # Switch to the iframe context
    driver.switch_to.frame(iframe)

    # Mute Volumn
    volumn_button = driver.find_element(By.XPATH, '//*[@id="player"]/div[7]/div[8]/div[2]/div/div[2]/button')
    volumn_button.click()

    # Press Play
    play_button = driver.find_element(By.XPATH, '//*[@id="player"]/div[7]/div[8]/div[1]/button')
    play_button.click()

    # Let player play for a few seconds
    time.sleep(3)

    # Locate the video's time bar
    time_bar = driver.find_element(By.XPATH, '//*[@id="player"]/div[7]/div[8]/div[2]/div/div[1]/div/div[1]')

    # Get current play time
    aria_valuetext = time_bar.get_attribute('aria-valuetext')

    # Assert playtime is not 0
    assert aria_valuetext != "00:00 of 02:05"

    # Switch back to the default content
    driver.switch_to.default_content()


def test_submit_contact_form(driver):
    """
    Description:
    Asserts contact form success after submitting name and email

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns: -
    """
    # Fill name box
    name_box = driver.find_element(By.XPATH, '//*[@id="form-field-name"]')
    name_box.clear()
    name_box.send_keys("John Doe")

    # Fill email box
    email_box = driver.find_element(By.XPATH, '//*[@id="form-field-email"]')
    email_box.clear()
    email_box.send_keys("johndoe@johndoe.com")

    # Click 'Submit'
    driver.find_element(By.XPATH, '//*[@id="contact_us_homepage"]/div/div[6]/button').click()

    # Wait for the result to be visible
    result = WebDriverWait(driver, 3).until(
        EC.visibility_of_element_located((By.XPATH, '//*[@id="contact_us_homepage"]/div[2]'))
    )

    # Assert result
    assert 'Your submission was successful.' in result.text


def test_top_page_header(driver):
    element = _bring_element_into_view(driver, '//*[@id="content"]/div/div/section[1]/div[4]/div/div/section[1]/div/div[1]/div/div[1]/div/h1')
    assert 'Transforming\nThe Care Experience' in element.text


def test_mid_page_header(driver):
    element = _bring_element_into_view(driver, '//*[@id="content"]/div/div/section[2]/div[3]/div/div/section/div[2]/div/div/div[3]/div/h2')
    assert 'Quality, Safety, Engagement' in element.text


def test_bottom_page_header(driver):
    element = _bring_element_into_view(driver, '//*[@id="content"]/div/div/section[5]/div/div/div/div[3]/div/h2')
    assert 'Improving Outcomes' in element.text