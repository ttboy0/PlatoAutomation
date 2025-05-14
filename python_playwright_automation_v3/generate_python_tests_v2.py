import os
import re
import pandas as pd

PYTHON_PROJECT_DIR = "/home/ubuntu/python_playwright_automation_v3"
DATA_DIR = os.path.join(PYTHON_PROJECT_DIR, "data")
TESTS_DIR = os.path.join(PYTHON_PROJECT_DIR, "tests")
COMMON_MODULE_PATH = "common"

def sanitize_test_name(name):
    name = re.sub(r"[^a-zA-Z0-9_]+", "_", name)
    name = name.strip("_").lower()
    if not name:
        return "element"
    return name[:50]

def generate_python_test_file(csv_file_path, page_name):
    test_file_name = f"test_{page_name}.py"
    test_file_path = os.path.join(TESTS_DIR, test_file_name)

    try:
        elements_df = pd.read_csv(csv_file_path)
        if elements_df.empty:
            print(f"Skipping {test_file_name} as CSV {csv_file_path} is empty.")
            with open(test_file_path, "w") as f:
                f.write("import pytest\n\n")
                f.write("# This test file is empty because its corresponding CSV was empty.\n")
                f.write("def test_empty_page_data():\n")
                f.write("    pytest.skip(\"Skipping test as no data was provided for this page.\")\n")
            return
        elements = elements_df.to_dict("records")
    except pd.errors.EmptyDataError:
        print(f"Skipping {test_file_name} as CSV {csv_file_path} is empty or unreadable.")
        with open(test_file_path, "w") as f:
            f.write("import pytest\n\n")
            f.write("# This test file is empty because its corresponding CSV was empty or unreadable.\n")
            f.write("def test_empty_or_unreadable_page_data():\n")
            f.write("    pytest.skip(\"Skipping test as no data was provided or CSV was unreadable for this page.\")\n")
        return
    except FileNotFoundError:
        print(f"CSV file {csv_file_path} not found. Skipping test generation for {page_name}.")
        return

    if not elements:
        print(f"No elements found in {csv_file_path} after loading. Skipping test generation for {page_name}.")
        with open(test_file_path, "w") as f:
            f.write("import pytest\n\n")
            f.write("# This test file is empty because its corresponding CSV was empty or contained no elements.\n")
            f.write("def test_no_elements_in_page_data():\n")
            f.write("    pytest.skip(\"Skipping test as no elements were provided in the data for this page.\")\n")
        return

    page_url = str(elements[0].get("page_url", ""))
    if not page_url:
        print(f"Could not determine PAGE_URL from {csv_file_path}. Skipping test generation for {page_name}.")
        return

    with open(test_file_path, "w") as f:
        f.write("import pytest\n")
        f.write("from playwright.sync_api import Page\n")
        f.write(f"from {COMMON_MODULE_PATH} import load_csv_data, navigate_to_url, verify_link_element, verify_content_element\n")
        f.write("import os\n\n")

        f.write(f"PAGE_URL = \"{page_url}\"\n")
        f.write(f"DATA_FILE = os.path.join(os.path.dirname(__file__), \"..\", \"data\", \"{os.path.basename(csv_file_path)}\")\n\n")
        
        f.write("@pytest.fixture(scope=\"module\")\n")
        f.write("def page_elements_data():\n")
        f.write("    data = load_csv_data(DATA_FILE)\n")
        f.write("    if not data:\n")
        f.write(f"        pytest.skip(f\"Skipping all tests in this file as no data could be loaded from {{DATA_FILE}}.\")\n")
        f.write("    return data\n\n")

        for i, element_data_in_loop in enumerate(elements):
            element_type = element_data_in_loop.get("element_type", "unknown")
            element_text_for_name = str(element_data_in_loop.get("text", ""))
            element_selector_for_name = str(element_data_in_loop.get("selector_css", ""))
            
            if not element_text_for_name.strip() and element_selector_for_name.strip():
                base_name = element_selector_for_name
            else:
                base_name = element_text_for_name
            if not base_name.strip():
                 base_name = f"{element_type}_item_{i}"

            test_name = sanitize_test_name(f"{element_type}_{base_name}")
            
            f.write(f"def test_{test_name}_{i}(page: Page, page_elements_data):\n")
            f.write("    # Ensure data for this specific test exists in the loaded data for the page\n")
            f.write(f"    if len(page_elements_data) <= {i}:\n")
            f.write(f"        pytest.skip(f\"Skipping test_{test_name}_{i} as data for index {i} is not available in the loaded data from {{DATA_FILE}}.\")\n")
            f.write(f"    current_element_data = page_elements_data[{i}]\n")
            f.write("    \n")
            f.write("    # Navigate to the page for each test to ensure a clean state\n")
            f.write(f"    if not navigate_to_url(page, PAGE_URL):\n")
            f.write(f"        pytest.fail(f\"Failed to navigate to {{PAGE_URL}} for test_{test_name}_{i}.\")\n")
            f.write("    \n")
            actual_element_type = element_data_in_loop.get("element_type", "unknown")
            if actual_element_type == "link":
                f.write(f"    verify_link_element(page, current_element_data)\n")
            elif actual_element_type == "content":
                f.write(f"    verify_content_element(page, current_element_data)\n")
            else:
                f.write(f"    pytest.skip(f\"Unsupported element type: {{actual_element_type}} in {{DATA_FILE}} for index {i}.\")\n")
            f.write("\n")
            
    print(f"Generated Python test file: {test_file_path}")

def main():
    os.makedirs(TESTS_DIR, exist_ok=True)
    init_py_tests = os.path.join(TESTS_DIR, "__init__.py")
    if not os.path.exists(init_py_tests):
        with open(init_py_tests, "w") as f:
            f.write("# This file makes Python treat the directory as a package.\n")
        print(f"Created {init_py_tests}")

    init_py_root = os.path.join(PYTHON_PROJECT_DIR, "__init__.py")
    if not os.path.exists(init_py_root):
        with open(init_py_root, "w") as f:
            f.write("# This file makes Python treat the directory as a package.\n")
        print(f"Created {init_py_root}")

    for item in os.listdir(TESTS_DIR):
        if item.startswith("test_") and item.endswith(".py"):
            os.remove(os.path.join(TESTS_DIR, item))
            print(f"Removed old test file: {item}")

    for file_name in os.listdir(DATA_DIR):
        if file_name.endswith("_data.csv") and not file_name.endswith("_archived_data.csv"):
            page_name_match = re.match(r"(.+)_data\.csv", file_name) # Corrected regex for literal dot
            if page_name_match:
                page_name = page_name_match.group(1)
                csv_file_path = os.path.join(DATA_DIR, file_name)
                generate_python_test_file(csv_file_path, page_name)

if __name__ == "__main__":
    main()

