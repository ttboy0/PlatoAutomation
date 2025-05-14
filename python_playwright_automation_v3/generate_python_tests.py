import os
import re

PYTHON_PROJECT_DIR = "/home/ubuntu/python_playwright_automation_v3"
DATA_DIR = os.path.join(PYTHON_PROJECT_DIR, "data")
TEST_DIR = PYTHON_PROJECT_DIR # Tests will be in the root of the project

# Ensure the main project directory and test directory exist
os.makedirs(TEST_DIR, exist_ok=True)

PYTHON_TEST_TEMPLATE = """
import pytest
from playwright.sync_api import Page, Browser # Import Browser
import pandas as pd
import os
import common # Assuming common.py is in the same directory or PYTHONPATH

CSV_FILENAME = \"{csv_filename}\" # Filled by outer format
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "data", CSV_FILENAME)

TEST_DATA = common.load_data_from_csv(CSV_PATH)
PAGE_URL = TEST_DATA[\"page_url\"].iloc[0] if not TEST_DATA.empty and \"page_url\" in TEST_DATA.columns else None

@pytest.fixture(scope=\"module\")
def module_page(browser: Browser) -> Page:
    if not PAGE_URL:
        pytest.skip(f\"PAGE_URL is not defined or CSV is empty/missing page_url for {{CSV_FILENAME}}, skipping all tests in this module.\")
    
    page = browser.new_page()
    common.logger.info(f\"Module setup for {{CSV_FILENAME}}: Navigating to {{PAGE_URL}} once for all tests in this file.\")
    common.navigate_to_url(page, PAGE_URL) # This will log redirects etc.
    yield page # Provide the page to tests
    page.close() # Teardown: close page after all tests in module are done

@pytest.mark.parametrize(\"test_case\", TEST_DATA.to_dict(\"records\"))
def test_{page_name}_elements(module_page: Page, test_case: dict): # Use the module-scoped page
    # No need to navigate again here, module_page is already on PAGE_URL
    page = module_page # Use the page from the module-scoped fixture

    element_type = test_case.get(\"element_type\")
    expected_text = str(test_case.get(\"text\", \"\")).strip()
    expected_href = str(test_case.get(\"href\", \"\")).strip()
    locator_type = str(test_case.get(\"locator_type\", \"\")).strip()
    locator_value = str(test_case.get(\"locator_value\", \"\")).strip()
    tag_name = str(test_case.get(\"tag_name\", \"\")).strip()

    common.logger.info(f\"Testing on page: {{PAGE_URL}} - Element type: {{element_type}} - Text: \t\'{{expected_text}}\'\")

    if element_type == \"link\":
        assert common.verify_link(page, expected_text, expected_href, locator_type, locator_value), \
            f\"Link verification failed for text: \t\'{{expected_text}}\' with href \t\'{{expected_href}}\' on page {{PAGE_URL}}\"
    elif element_type == \"content\":
        assert common.verify_content_element(page, expected_text, locator_type, locator_value, tag_name), \
            f\"Content verification failed for text: \t\'{{expected_text}}\' with tag \t\'{{tag_name}}\' on page {{PAGE_URL}}\"
    else:
        common.logger.warning(f\"Unknown element type: {{element_type}} for text \t\'{{expected_text}}\' on page {{PAGE_URL}}\")
        pytest.skip(f\"Skipping unknown element type: {{element_type}}\")

"""

def generate_python_tests_main():
    print("Generator script: Starting Python test file generation (optimized for single page load per file)...")
    if not os.path.exists(DATA_DIR):
        print(f"Generator script: Data directory not found: {DATA_DIR}")
        return

    for item in os.listdir(TEST_DIR):
        if item.startswith("test_") and item.endswith(".py") and item != "common.py" and item != "generate_python_tests.py": # Avoid deleting self or common
            try:
                os.remove(os.path.join(TEST_DIR, item))
                print(f"Generator script: Removed old test file: {item}")
            except OSError as e:
                print(f"Generator script: Error removing old test file {item}: {e}")

    for csv_file in os.listdir(DATA_DIR):
        if csv_file.endswith("_data.csv"):
            page_name_match = re.match(r"(.+)_data\.csv", csv_file)
            if page_name_match:
                page_name = page_name_match.group(1)
                sanitized_page_name = re.sub(r"\W|^(?=\d)", "_", page_name)
                if not sanitized_page_name:
                    sanitized_page_name = "generic_page"
                
                test_file_name = f"test_{sanitized_page_name}.py"
                test_file_path = os.path.join(TEST_DIR, test_file_name)

                print(f"Generator script: Generating test file for {page_name} (as {sanitized_page_name}): {test_file_path} from {csv_file}")

                test_content = PYTHON_TEST_TEMPLATE.format(
                    page_name=sanitized_page_name,
                    csv_filename=csv_file 
                )

                try:
                    with open(test_file_path, "w") as f:
                        f.write(test_content)
                    print(f"Generator script: Successfully generated {test_file_path}")
                except IOError as e:
                    print(f"Generator script: Failed to write test file {test_file_path}: {e}")
            else:
                print(f"Generator script: Could not extract page name from CSV file: {csv_file}")
        else:
            print(f"Generator script: Skipping non-data CSV file: {csv_file}")
    print("Generator script: Python test file generation completed.")

if __name__ == "__main__":
    generate_python_tests_main()

