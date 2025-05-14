import pytest
from playwright.sync_api import Page
from ..common import load_csv_data, navigate_to_url, verify_link_element, verify_content_element
import os

# Define the path to the CSV data file relative to the test file
CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "../data/services_data.csv")

# Load the test data from CSV
TEST_DATA = load_csv_data(CSV_FILE_PATH)

# Define the base URL for the services page
SERVICES_PAGE_URL = "https://platotech.com/services/"

@pytest.fixture(scope="function")
def setup_page(page: Page):
    assert navigate_to_url(page, SERVICES_PAGE_URL), f"Failed to navigate to {SERVICES_PAGE_URL}"
    return page # The fixture now returns the navigated page object

# Dynamically create test functions for each element in the CSV
for i, element_data in enumerate(TEST_DATA):
    element_type = element_data.get("element_type", "unknown").lower()
    element_text_or_id = str(element_data.get("text", element_data.get("id", f"element_{i}"))).strip()
    sanitized_name = "".join(c if c.isalnum() else "_" for c in element_text_or_id).lower()
    
    test_name = f"test_{element_type}_{sanitized_name}_{i}"

    if element_type == "link":
        # The test function now accepts setup_page (which is the navigated page object)
        def test_link_func(setup_page: Page, data=element_data):
            # No need to call setup_page(page) here, fixture handles it.
            # The 'page' to use for verification is the one returned by the fixture, i.e., setup_page
            assert verify_link_element(setup_page, data), f"Verification failed for link: {data.get('selector')}"
        exec(f"{test_name} = test_link_func")
    elif element_type == "content":
        # The test function now accepts setup_page (which is the navigated page object)
        def test_content_func(setup_page: Page, data=element_data):
            # No need to call setup_page(page) here, fixture handles it.
            # The 'page' to use for verification is the one returned by the fixture, i.e., setup_page
            assert verify_content_element(setup_page, data), f"Verification failed for content: {data.get('selector')}"
        exec(f"{test_name} = test_content_func")
    else:
        print(f"Skipping unknown element type: {element_type} for element {element_text_or_id}")

