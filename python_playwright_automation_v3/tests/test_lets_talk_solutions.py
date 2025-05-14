import pytest
from playwright.sync_api import Page
from common import load_csv_data, navigate_to_url, verify_link_element, verify_content_element
import os

PAGE_URL = "https://platotech.com/lets-talk-solutions/"
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "lets_talk_solutions_data.csv")

@pytest.fixture(scope="module")
def page_elements_data():
    data = load_csv_data(DATA_FILE)
    if not data:
        pytest.skip(f"Skipping all tests in this file as no data could be loaded from {DATA_FILE}.")
    return data

def test_link_plato_logo_0(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 0:
        pytest.skip(f"Skipping test_link_plato_logo_0 as data for index 0 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[0]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_link_plato_logo_0.")
    
    verify_link_element(page, current_element_data)

def test_link_nan_1(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 1:
        pytest.skip(f"Skipping test_link_nan_1 as data for index 1 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[1]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_link_nan_1.")
    
    verify_link_element(page, current_element_data)

