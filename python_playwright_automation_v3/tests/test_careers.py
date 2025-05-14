import pytest
from playwright.sync_api import Page
from common import load_csv_data, navigate_to_url, verify_link_element, verify_content_element
import os

PAGE_URL = "https://platotech.com/careers/"
DATA_FILE = os.path.join(os.path.dirname(__file__), "..", "data", "careers_data.csv")

@pytest.fixture(scope="module")
def page_elements_data():
    data = load_csv_data(DATA_FILE)
    if not data:
        pytest.skip(f"Skipping all tests in this file as no data could be loaded from {DATA_FILE}.")
    return data

def test_link_test_automation_0(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 0:
        pytest.skip(f"Skipping test_link_test_automation_0 as data for index 0 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[0]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_link_test_automation_0.")
    
    verify_link_element(page, current_element_data)

def test_link_functional_testing_1(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 1:
        pytest.skip(f"Skipping test_link_functional_testing_1 as data for index 1 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[1]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_link_functional_testing_1.")
    
    verify_link_element(page, current_element_data)

def test_link_performance_testing_2(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 2:
        pytest.skip(f"Skipping test_link_performance_testing_2 as data for index 2 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[2]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_link_performance_testing_2.")
    
    verify_link_element(page, current_element_data)

def test_link_enterprise_resource_planning_erp_testing_3(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 3:
        pytest.skip(f"Skipping test_link_enterprise_resource_planning_erp_testing_3 as data for index 3 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[3]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_link_enterprise_resource_planning_erp_testing_3.")
    
    verify_link_element(page, current_element_data)

def test_content_test_automation_4(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 4:
        pytest.skip(f"Skipping test_content_test_automation_4 as data for index 4 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[4]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_content_test_automation_4.")
    
    verify_content_element(page, current_element_data)

def test_content_functional_testing_5(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 5:
        pytest.skip(f"Skipping test_content_functional_testing_5 as data for index 5 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[5]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_content_functional_testing_5.")
    
    verify_content_element(page, current_element_data)

def test_content_performance_testing_6(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 6:
        pytest.skip(f"Skipping test_content_performance_testing_6 as data for index 6 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[6]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_content_performance_testing_6.")
    
    verify_content_element(page, current_element_data)

def test_content_enterprise_resource_planning_erp_testing_7(page: Page, page_elements_data):
    # Ensure data for this specific test exists in the loaded data for the page
    if len(page_elements_data) <= 7:
        pytest.skip(f"Skipping test_content_enterprise_resource_planning_erp_testing_7 as data for index 7 is not available in the loaded data from {DATA_FILE}.")
    current_element_data = page_elements_data[7]
    
    # Navigate to the page for each test to ensure a clean state
    if not navigate_to_url(page, PAGE_URL):
        pytest.fail(f"Failed to navigate to {PAGE_URL} for test_content_enterprise_resource_planning_erp_testing_7.")
    
    verify_content_element(page, current_element_data)

