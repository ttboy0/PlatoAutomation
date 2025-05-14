const fs = require("fs");
const path = require("path");

const JS_PROJECT_DIR = "/home/ubuntu/javascript_playwright_automation_v3";
const DATA_DIR = path.join(JS_PROJECT_DIR, "data");
const TEST_DIR = path.join(JS_PROJECT_DIR, "tests");

// Ensure the tests directory exists
if (!fs.existsSync(TEST_DIR)) {
    fs.mkdirSync(TEST_DIR, { recursive: true });
}

const JS_TEST_TEMPLATE = `
const { test, expect } = require("@playwright/test");
const path = require("path");
const { logger, navigateToUrl, loadDataFromCsv, verifyLink, verifyContentElement } = require("../utils/common.js");

const CSV_FILENAME = "{csv_filename}";
const CSV_PATH = path.join(__dirname, "..", "data", CSV_FILENAME);

const TEST_DATA = loadDataFromCsv(CSV_PATH);
const PAGE_URL = TEST_DATA.length > 0 && TEST_DATA[0].page_url ? TEST_DATA[0].page_url : null;

test.describe("Page: {page_name_description}", () => {

    if (!PAGE_URL) {
        logger.warning('Skipping test generation for {page_name_description} as PAGE_URL is not defined in ' + CSV_FILENAME + '.');
    } else {
        TEST_DATA.forEach((testCase, index) => {
            const currentElementType = String(testCase.element_type || "").trim();
            const currentExpectedText = String(testCase.text || "").trim();

            if (currentElementType !== "link" && currentElementType !== "content") {
                logger.warning('Unknown element type: "' + currentElementType + '" for text "' + currentExpectedText + '" on page ' + PAGE_URL + '. Skipping this test case.');
                return;
            }

            test('Test Case #' + (index + 1) + ': ' + currentElementType + ' - ' + currentExpectedText.substring(0, 70).replace(/\'/g, "\\'").replace(/\"/g, "\\\"") + '...', async ({ page }) => {
                await navigateToUrl(page, PAGE_URL);

                const elementType = currentElementType;
                const expectedText = currentExpectedText;
                const expectedHref = String(testCase.href || "").trim();
                const locatorType = String(testCase.locator_type || "").trim();
                const locatorValue = String(testCase.locator_value || "").trim();
                const tagName = String(testCase.tag_name || "").trim();

                logger.info('Testing on page: ' + PAGE_URL + ' - Element type: ' + elementType + ' - Text: \t\'' + expectedText.replace(/\'/g, "\\'") + '\'\t');

                let success = false;
                if (elementType === "link") {
                    success = await verifyLink(page, expectedText, expectedHref, locatorType, locatorValue);
                    expect(success, 
                        'Link verification failed for text: \t\'' + expectedText.replace(/\'/g, "\\'") + '\'\t with href \t\'' + expectedHref.replace(/\'/g, "\\'") + '\'\t on page \t' + PAGE_URL
                    ).toBe(true);
                } else if (elementType === "content") {
                    success = await verifyContentElement(page, expectedText, locatorType, locatorValue, tagName);
                    expect(success, 
                        'Content verification failed for text: \t\'' + expectedText.replace(/\'/g, "\\'") + '\'\t with tag \t\'' + tagName.replace(/\'/g, "\\'") + '\'\t on page \t' + PAGE_URL
                    ).toBe(true);
                }
            });
        });
    }
});
`;

function generateJavaScriptTests() {
    console.log("Generator script: Starting JavaScript test file generation...");
    if (!fs.existsSync(DATA_DIR)) {
        console.log("Generator script: Data directory not found: " + DATA_DIR);
        return;
    }

    fs.readdirSync(TEST_DIR).forEach(file => {
        if (file.endsWith(".spec.js")) {
            fs.unlinkSync(path.join(TEST_DIR, file));
            console.log("Generator script: Removed old test file: " + file);
        }
    });

    fs.readdirSync(DATA_DIR).forEach(csvFile => {
        if (csvFile.endsWith("_data.csv")) {
            const pageNameMatch = csvFile.match(/(.+)_data\.csv/);
            if (pageNameMatch) {
                const pageName = pageNameMatch[1];
                const sanitizedPageName = pageName.replace(/\W/g, '_');
                const pageNameDescription = pageName.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase());

                const testFileName = `${sanitizedPageName}.spec.js`;
                const testFilePath = path.join(TEST_DIR, testFileName);

                console.log("Generator script: Generating test file for " + pageName + " (as " + sanitizedPageName + "): " + testFilePath + " from " + csvFile);

                const testContent = JS_TEST_TEMPLATE
                    .replace(/{page_name_description}/g, pageNameDescription)
                    .replace(/{csv_filename}/g, csvFile);

                try {
                    fs.writeFileSync(testFilePath, testContent);
                    console.log("Generator script: Successfully generated " + testFilePath);
                } catch (e) {
                    console.error("Generator script: Failed to write test file " + testFilePath + ": " + e.message);
                }
            } else {
                console.log("Generator script: Could not extract page name from CSV file: " + csvFile);
            }
        } else {
            console.log("Generator script: Skipping non-data CSV file: " + csvFile);
        }
    });
    console.log("Generator script: JavaScript test file generation completed.");
}

if (require.main === module) {
    generateJavaScriptTests();
}

