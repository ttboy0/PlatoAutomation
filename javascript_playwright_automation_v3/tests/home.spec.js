const { test, expect } = require("@playwright/test");
const path = require("path");
const {
    loadCsvData,
    navigateToUrl,
    verifyLinkElement,
    verifyContentElement,
} = require("../utils/common.js");

// Define the path to the CSV data file
const csvFilePath = path.join(__dirname, "../data/homepage_data.csv");

// Load the test data from CSV
const testData = loadCsvData(csvFilePath);

// Define the base URL for the homepage
const HOMEPAGE_URL = "https://platotech.com/";

test.describe("Platotech Homepage Automation (JavaScript)", () => {
    // Hook to navigate to the homepage before each test in this describe block
    test.beforeEach(async ({ page }) => {
        await navigateToUrl(page, HOMEPAGE_URL);
    });

    // Dynamically create tests based on CSV data
    for (const element of testData) {
        if (!element || !element.selector || !element.element_type) {
            console.warn("Skipping invalid test data row:", element);
            continue;
        }

        const testTitle = `Verify ${element.element_type}: "${element.text || element.selector}"`;

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
                throw error; // Re-throw to mark the test as failed in Playwright report
            }
        });
    }
});

