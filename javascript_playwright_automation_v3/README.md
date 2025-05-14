# Platotech Website Automation (JavaScript Playwright)

This project provides an automated testing framework for the Platotech website (https://platotech.com/) using JavaScript and Playwright.

## Project Structure

```
javascript_playwright_automation_v3/
├── data/                     # CSV files containing test data for different pages
│   ├── homepage_data.csv
│   └── services_data.csv
├── playwright-report/        # HTML reports from Playwright test executions
├── tests/
│   ├── home.spec.js
│   └── services.spec.js
├── utils/
│   └── common.js             # Common functions for test automation (CSV loading, navigation, verification)
├── .gitignore
├── package.json              # npm project configuration and dependencies
├── package-lock.json         # npm lock file
└── README.md                 # This file
```

## Prerequisites

*   Node.js (version 16.x or higher recommended; this project was tested with Node.js 20.x)
*   npm (usually comes with Node.js)

## Setup Instructions

1.  **Clone the repository (or ensure project files are in place).**

2.  **Navigate to the project directory:**
    ```bash
    cd /path/to/javascript_playwright_automation_v3
    ```

3.  **Install dependencies using npm:**
    ```bash
    npm install
    ```
    This will install Playwright and other necessary packages as defined in `package.json`.

4.  **Install Playwright browsers:**
    ```bash
    npx playwright install
    ```
    This command downloads the browser binaries (Chromium, Firefox, WebKit) that Playwright uses.

## Running Tests

1.  **Run all tests:**
    ```bash
    npx playwright test
    ```

2.  **Run tests for a specific page (e.g., homepage):**
    ```bash
    npx playwright test tests/home.spec.js
    ```

3.  **View the HTML report:**
    After running tests, Playwright automatically generates an HTML report in the `playwright-report` directory. You can open it with:
    ```bash
    npx playwright show-report
    ```
    This will typically open the report in your default web browser.

## Important Considerations

### Link Validation and 403 Errors

*   When validating links, simply sending a HEAD request to check a link's status can sometimes result in a **403 Forbidden** error. Some websites, including Platotech for certain paths, may block these types of automated requests.
*   **Solution Implemented**: The `utils/common.js` script in this project uses Playwright's full navigation capabilities (opening the link in a new page context) to verify link accessibility. This method is more robust as it emulates a real user visiting the page and is less likely to be blocked. This approach is used in the `verifyLinkElement` function.

## Adding Validation for a New Page

If you want to add automated tests for a new page on the Platotech website using the JavaScript framework, follow these steps:

1.  **Identify Elements for Testing:**
    *   Manually navigate to the new page (e.g., `https://platotech.com/newpage/`).
    *   Identify 5-10 key, visible, and stable top-level elements you want to test (links, headings, text content, buttons, etc.).
    *   For each element, determine the most robust selector (prioritize `aria-label`, unique IDs, specific class names, or stable CSS selectors). Playwright also supports text-based selectors (e.g., `text=Click Me`).
    *   Note down the exact visible text for content elements and links, and the `href` attribute for links.

2.  **Create a CSV Data File:**
    *   In the `data/` directory, create a new CSV file named `newpage_data.csv` (replace `newpage` with the actual page name, e.g., `training_data.csv`).
    *   The CSV file must have the following header row:
        `element_type,selector,text,href,id,classes,aria_label`
    *   Add a row for each element you identified. Populate the columns:
        *   `element_type`: `link` or `content`.
        *   `selector`: The CSS or Playwright selector (e.g., `h1.main-title`, `a[href="/contact-us"]`, `#unique-button`, `text=Submit Form`).
        *   `text`: The exact visible text of the element. For logos, you can use a descriptive name like "PLATO Logo".
        *   `href`: The full URL the link points to. Leave as `nan` or empty if not a link.
        *   `id`, `classes`, `aria_label`: Optional. Populate if key to selector strategy or for documentation. Otherwise, `nan` or empty.
    *   **Important for Selectors in CSV**: If your selector string contains commas, you *must* enclose the entire selector string in double quotes in the CSV. For example: `"div.parent, span.child"`. The `common.js` script includes logic to handle parsing these quoted selectors correctly.
    *   Example row for a link:
        `link,a.contact-link,Contact Us,https://platotech.com/contact-us/,nan,contact-link,nan`
    *   Example row for content with a Playwright text selector:
        `content,"h1.page-title >> text=About Our Company",About Our Company,nan,main-title,page-title,nan`

3.  **Create a New Test Spec File:**
    *   In the `tests/` directory, create a new JavaScript file, e.g., `newpage.spec.js`.
    *   Use the following template, adapting it for your new page:
        ```javascript
        const { test, expect } = require("@playwright/test");
        const path = require("path");
        const {
            loadCsvData,
            navigateToUrl,
            verifyLinkElement,
            verifyContentElement,
        } = require("../utils/common.js");

        // Define the path to your new CSV data file
        const csvFilePath = path.join(__dirname, "../data/newpage_data.csv");

        // Load the test data from CSV
        const testData = loadCsvData(csvFilePath);

        // Define the URL for the new page
        const NEW_PAGE_URL = "https://platotech.com/newpage/"; // Replace with actual URL

        test.describe("Platotech NewPage Automation (JavaScript)", () => {
            test.beforeEach(async ({ page }) => {
                await navigateToUrl(page, NEW_PAGE_URL);
            });

            for (const element of testData) {
                if (!element || !element.selector || !element.element_type) {
                    console.warn("Skipping invalid test data row:", element);
                    continue;
                }

                const testTitle = `Verify ${element.element_type}: "${element.text || element.id || element.selector}"`;

                test(testTitle, async ({ page }) => {
                    console.log(`Starting test: ${testTitle}`);
                    try {
                        if (element.element_type === "link") {
                            await verifyLinkElement(page, element);
                        } else if (element.element_type === "content") {
                            await verifyContentElement(page, element);
                        } else {
                            throw new Error(`Unknown element_type: ${element.element_type} for selector ${element.selector}`);
                        }
                        console.log(`Test PASSED: ${testTitle}`);
                    } catch (error) {
                        console.error(`Test FAILED: ${testTitle} with error: ${error.message}`);
                        throw error; // Re-throw to mark the test as failed
                    }
                });
            }
        });
        ```

4.  **Run Your New Tests:**
    ```bash
    npx playwright test tests/newpage.spec.js
    ```

5.  **Review and Refine:**
    *   Check the HTML report (`npx playwright show-report`).
    *   If there are failures, debug your selectors or expected data in the CSV file. Ensure elements are consistently found and validated.

By following these steps, you can extend the JavaScript test suite to cover new pages of the Platotech website.

