
import pytest
from playwright.sync_api import Page, Browser # Import Browser
import pandas as pd
import os
import common # Assuming common.py is in the same directory or PYTHONPATH

CSV_FILENAME = "resources_data.csv" # Filled by outer format
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", CSV_FILENAME)

TEST_DATA = common.load_data_from_csv(CSV_PATH)
PAGE_URL = TEST_DATA["page_url"].iloc[0] if not TEST_DATA.empty and "page_url" in TEST_DATA.columns else None

@pytest.fixture(scope="module")
def module_page(browser: Browser) -> Page:
    if not PAGE_URL:
        pytest.skip(f"PAGE_URL is not defined or CSV is empty/missing page_url for {CSV_FILENAME}, skipping all tests in this module.")
    
    page = browser.new_page()
    common.logger.info(f"Module setup for {CSV_FILENAME}: Navigating to {PAGE_URL} once for all tests in this file.")
    common.navigate_to_url(page, PAGE_URL) # This will log redirects etc.
    yield page # Provide the page to tests
    page.close() # Teardown: close page after all tests in module are done

@pytest.mark.parametrize("test_case", TEST_DATA.to_dict("records"))
def test_resources_elements(module_page: Page, test_case: dict): # Use the module-scoped page
    # No need to navigate again here, module_page is already on PAGE_URL
    page = module_page # Use the page from the module-scoped fixture

    element_type = test_case.get("element_type")
    expected_text = str(test_case.get("text", "")).strip()
    expected_href = str(test_case.get("href", "")).strip()
    locator_type = str(test_case.get("locator_type", "")).strip()
    locator_value = str(test_case.get("locator_value", "")).strip()
    tag_name = str(test_case.get("tag_name", "")).strip()

    common.logger.info(f"Testing on page: {PAGE_URL} - Element type: {element_type} - Text: 	'{expected_text}'")

    if element_type == "link":
        assert common.verify_link(page, expected_text, expected_href, locator_type, locator_value),             f"Link verification failed for text: 	'{expected_text}' with href 	'{expected_href}' on page {PAGE_URL}"
    elif element_type == "content":
        assert common.verify_content_element(page, expected_text, locator_type, locator_value, tag_name),             f"Content verification failed for text: 	'{expected_text}' with tag 	'{tag_name}' on page {PAGE_URL}"
    else:
        common.logger.warning(f"Unknown element type: {element_type} for text 	'{expected_text}' on page {PAGE_URL}")
        pytest.skip(f"Skipping unknown element type: {element_type}")

