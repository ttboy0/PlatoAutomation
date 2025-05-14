// @ts-check
const { test, expect } = require("@playwright/test");
const path = require("path");
const { loadCsvData, navigateToUrl, verifyLinkElement, verifyContentElement, logger } = require("../utils/common.js");

const PAGE_URL = "https://platotech.com/careers/";
const DATA_FILE = path.join(__dirname, "..", "data", "careers_data.csv");

test.describe.configure({ mode: "parallel" }); // Enable parallel execution for tests within this file

test.describe("careers page tests", () => {
    let pageElementsData;
    let sharedPage;

    test.beforeAll(async ({ browser }) => {
        logger.info("Running beforeAll hook for careers");
        pageElementsData = await loadCsvData(DATA_FILE);
        if (!pageElementsData || pageElementsData.length === 0) {
            logger.warn("No data loaded for careers, tests in this file might be skipped or fail.");
            // No need to create page if no data
            return;
        }
        sharedPage = await browser.newPage();
        const navigationSuccess = await navigateToUrl(sharedPage, PAGE_URL);
        if (!navigationSuccess) {
            logger.error("Failed to navigate in beforeAll for careers, subsequent tests may fail.");
            // Optionally, throw an error to stop tests if navigation is critical
            // throw new Error("Failed to navigate to page in beforeAll");
        }
    });

    test.afterAll(async () => {
        logger.info("Running afterAll hook for careers");
        if (sharedPage) {
            await sharedPage.close();
        }
    });

    if (!fs.existsSync(DATA_FILE) || fs.readFileSync(DATA_FILE, "utf-8").trim() === "") {
        test("data_file_empty_or_missing", async() => {
            logger.warn("Data file is empty or missing, skipping actual tests for careers.");
            test.skip(true, "Data file is empty or missing.");
        });
    } else {
        test("link_test_automation_0", async () => {
            if (!sharedPage) test.skip(true, "Page setup failed in beforeAll or no data.");
            if (!pageElementsData || pageElementsData.length === 0) test.skip(true, "No test data loaded.");
            const currentElementData = pageElementsData[0];
            if (!currentElementData) test.skip(true, "Element data not found for this test index.");
            await verifyLinkElement(sharedPage, currentElementData, test);
        });

        test("link_functional_testing_1", async () => {
            if (!sharedPage) test.skip(true, "Page setup failed in beforeAll or no data.");
            if (!pageElementsData || pageElementsData.length === 0) test.skip(true, "No test data loaded.");
            const currentElementData = pageElementsData[1];
            if (!currentElementData) test.skip(true, "Element data not found for this test index.");
            await verifyLinkElement(sharedPage, currentElementData, test);
        });

        test("link_performance_testing_2", async () => {
            if (!sharedPage) test.skip(true, "Page setup failed in beforeAll or no data.");
            if (!pageElementsData || pageElementsData.length === 0) test.skip(true, "No test data loaded.");
            const currentElementData = pageElementsData[2];
            if (!currentElementData) test.skip(true, "Element data not found for this test index.");
            await verifyLinkElement(sharedPage, currentElementData, test);
        });

        test("link_enterprise_resource_planning_erp_testing_3", async () => {
            if (!sharedPage) test.skip(true, "Page setup failed in beforeAll or no data.");
            if (!pageElementsData || pageElementsData.length === 0) test.skip(true, "No test data loaded.");
            const currentElementData = pageElementsData[3];
            if (!currentElementData) test.skip(true, "Element data not found for this test index.");
            await verifyLinkElement(sharedPage, currentElementData, test);
        });

        test("content_test_automation_4", async () => {
            if (!sharedPage) test.skip(true, "Page setup failed in beforeAll or no data.");
            if (!pageElementsData || pageElementsData.length === 0) test.skip(true, "No test data loaded.");
            const currentElementData = pageElementsData[4];
            if (!currentElementData) test.skip(true, "Element data not found for this test index.");
            await verifyContentElement(sharedPage, currentElementData, test);
        });

        test("content_functional_testing_5", async () => {
            if (!sharedPage) test.skip(true, "Page setup failed in beforeAll or no data.");
            if (!pageElementsData || pageElementsData.length === 0) test.skip(true, "No test data loaded.");
            const currentElementData = pageElementsData[5];
            if (!currentElementData) test.skip(true, "Element data not found for this test index.");
            await verifyContentElement(sharedPage, currentElementData, test);
        });

        test("content_performance_testing_6", async () => {
            if (!sharedPage) test.skip(true, "Page setup failed in beforeAll or no data.");
            if (!pageElementsData || pageElementsData.length === 0) test.skip(true, "No test data loaded.");
            const currentElementData = pageElementsData[6];
            if (!currentElementData) test.skip(true, "Element data not found for this test index.");
            await verifyContentElement(sharedPage, currentElementData, test);
        });

        test("content_enterprise_resource_planning_erp_testing_7", async () => {
            if (!sharedPage) test.skip(true, "Page setup failed in beforeAll or no data.");
            if (!pageElementsData || pageElementsData.length === 0) test.skip(true, "No test data loaded.");
            const currentElementData = pageElementsData[7];
            if (!currentElementData) test.skip(true, "Element data not found for this test index.");
            await verifyContentElement(sharedPage, currentElementData, test);
        });

    }
});
