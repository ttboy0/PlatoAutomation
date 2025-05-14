# Platotech Website Automation (Python Playwright)

This project provides an automated testing framework for the Platotech website (https://platotech.com/) using Python and Playwright.

## Project Structure

```
python_playwright_automation_v3/
├── data/                     # CSV files containing test data for different pages
│   ├── homepage_data.csv
│   └── services_data.csv
├── logs/                     # Log files from test executions
│   └── automation_python.log
├── tests/                    # Pytest test scripts
│   ├── __init__.py
│   ├── test_homepage.py
│   └── test_services.py
├── utils/                    # Utility scripts (if any, currently common functions are in common.py)
├── common.py                 # Common functions for test automation (navigation, verification)
├── conftest.py               # Pytest configuration, hooks for Playwright browser setup
├── generate_python_tests_v2.py # Script to generate test files from CSV data
├── .gitignore
├── Pipfile                   # Pipenv dependency file
├── Pipfile.lock
└── README.md                 # This file
```

## Prerequisites

*   Python 3.10 or higher (this project uses 3.11)
*   Pipenv (for managing dependencies)

## Setup Instructions

1.  **Clone the repository (or ensure project files are in place).**

2.  **Navigate to the project directory:**
    ```bash
    cd /path/to/python_playwright_automation_v3
    ```

3.  **Install dependencies using Pipenv:**
    If you don't have Pipenv, install it first: `pip install pipenv`
    ```bash
    pipenv install
    ```
    This will create a virtual environment and install all necessary packages, including Playwright and Pytest, as defined in the `Pipfile`.

4.  **Install Playwright browsers:**
    Activate the virtual environment: `pipenv shell`
    Then run:
    ```bash
    playwright install
    ```
    This command downloads the browser binaries (Chromium, Firefox, WebKit) that Playwright uses.

## Running Tests

1.  **Activate the virtual environment (if not already active):**
    ```bash
    pipenv shell
    ```

2.  **Run all tests:**
    ```bash
    pytest
    ```

3.  **Run tests for a specific page (e.g., homepage):**
    ```bash
    pytest tests/test_homepage.py
    ```

4.  **Generate an HTML report:**
    ```bash
    pytest --html=report.html --self-contained-html
    ```
    This will create a `report.html` file in the project root with detailed test results.

## Important Considerations

### Link Validation and 403 Errors

*   When validating links, simply sending a HEAD request (e.g., using the `requests` library) to check a link's status can sometimes result in a **403 Forbidden** error. Some websites, including Platotech for certain paths, may block these types of automated requests.
*   **Solution Implemented**: The `common.py` script in this project has been updated to use Playwright's full navigation capabilities (opening the link in a new page context) to verify link accessibility. This method is more robust as it emulates a real user visiting the page and is less likely to be blocked. This approach is used in the `verify_link_element` function.

## Adding Validation for a New Page

If you want to add automated tests for a new page on the Platotech website, follow these steps:

1.  **Identify Elements for Testing:**
    *   Manually navigate to the new page (e.g., `https://platotech.com/newpage/`).
    *   Identify 5-10 key, visible, and stable top-level elements you want to test. These can be links, headings, important text content, buttons, etc.
    *   For each element, determine the most robust selector (prioritize `aria-label`, unique IDs, specific class names, or stable CSS selectors). Avoid highly dynamic or generic selectors.
    *   Note down the exact visible text for content elements and links, and the `href` attribute for links.

2.  **Create a CSV Data File:**
    *   In the `data/` directory, create a new CSV file named `newpage_data.csv` (replace `newpage` with the actual page name, e.g., `training_data.csv`).
    *   The CSV file must have the following header row:
        `element_type,selector,text,href,id,classes,aria_label`
    *   Add a row for each element you identified. Populate the columns:
        *   `element_type`: `link` or `content`.
        *   `selector`: The CSS selector you identified (e.g., `h1.main-title`, `a[href="/contact-us"]`, `#unique-button`). For Playwright-specific selectors like text matching, you can use them (e.g., `h2.sub-heading >> text=Expected Text`).
        *   `text`: The exact visible text of the element. For logos or elements where text isn't the primary identifier, you can use a descriptive name like "PLATO Logo".
        *   `href`: The full URL the link points to. Leave as `nan` or empty if not a link.
        *   `id`, `classes`, `aria_label`: Optional. You can populate these if they were key to your selector strategy or for documentation. Otherwise, `nan` or empty.
    *   Example row for a link:
        `link,a.contact-link,Contact Us,https://platotech.com/contact-us/,nan,contact-link,nan`
    *   Example row for content:
        `content,h1.page-title,About Our Company,nan,main-title,page-title,nan`

3.  **Update the Test Generation Script (Optional but Recommended for Consistency):**
    *   Open `generate_python_tests_v2.py`.
    *   Modify the `PAGES_TO_AUTOMATE` list to include your new page configuration. For example:
        ```python
        PAGES_TO_AUTOMATE = [
            # ... existing pages ...
            {"name": "newpage", "url_path": "/newpage/", "csv_file": "newpage_data.csv"},
        ]
        ```
    *   Run the script: `python3.11 generate_python_tests_v2.py`
    *   This will create a new `tests/test_newpage.py` file based on your CSV.

4.  **Alternatively, Create the Test Script Manually:**
    *   If you prefer not to use the generator, create a new Python file in the `tests/` directory, e.g., `test_newpage.py`.
    *   Import necessary modules and functions:
        ```python
        import pytest
        import os
        from playwright.sync_api import Page
        from ..common import load_csv_data, navigate_to_url, verify_link_element, verify_content_element, BASE_URL

        PAGE_URL = BASE_URL + "/newpage/"
        CSV_FILE_PATH = os.path.join(os.path.dirname(__file__), "../data/newpage_data.csv")
        test_data = load_csv_data(CSV_FILE_PATH)

        @pytest.mark.parametrize("element_data", test_data)
        def test_newpage_elements(page: Page, element_data):
            navigate_to_url(page, PAGE_URL)
            element_type = element_data.get("element_type")
            if element_type == "link":
                verify_link_element(page, element_data)
            elif element_type == "content":
                verify_content_element(page, element_data)
            else:
                pytest.fail(f"Unknown element type: {element_type}")
        ```

5.  **Run Your New Tests:**
    ```bash
    pipenv shell
    pytest tests/test_newpage.py --html=report_newpage.html --self-contained-html
    ```

6.  **Review and Refine:**
    *   Check the test report. If there are failures, debug your selectors or expected data in the CSV file.
    *   Ensure elements are consistently found and validated.

By following these steps, you can extend the test suite to cover new pages of the Platotech website.

