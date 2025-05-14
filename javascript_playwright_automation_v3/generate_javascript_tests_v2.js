const fs = require("fs");
const path = require("path");
const { parse } = require("csv-parse/sync"); // Assuming this is installed or handled
const { execSync } = require("child_process"); // For running commands like reading CSV if needed

const JS_PROJECT_DIR = "/home/ubuntu/javascript_playwright_automation_v3";
const DATA_DIR = path.join(JS_PROJECT_DIR, "data");
const TESTS_DIR = path.join(JS_PROJECT_DIR, "tests");
const COMMON_MODULE_PATH = "../utils/common.js"; // Relative path from tests directory

function sanitizeTestName(name) {
    let sanitized = String(name).replace(/[^a-zA-Z0-9_]+/g, "_");
    sanitized = sanitized.replace(/^_+|_+$/g, "").toLowerCase();
    if (!sanitized) {
        return "element";
    }
    return sanitized.substring(0, 50);
}

function generateJsTestFile(csvFilePath, pageName) {
    const testFileName = `${pageName}.spec.js`;
    const testFilePath = path.join(TESTS_DIR, testFileName);
    let elements;

    try {
        const fileContent = fs.readFileSync(csvFilePath, { encoding: "utf-8" });
        const records = parse(fileContent, {
            columns: true,
            skip_empty_lines: true,
            trim: true
        });
        if (!records || records.length === 0) {
            console.log(`Skipping ${testFileName} as CSV ${csvFilePath} is empty.`);
            fs.writeFileSync(testFilePath, 
`// @ts-check
const { test, expect } = require("@playwright/test");

test.describe("${pageName} tests - (No data)", () => {
    test("skip_due_to_empty_data", async ({ page }) => {
        test.skip(true, "Skipping test as no data was provided for this page.");
    });
});
`);
            return;
        }
        elements = records;
    } catch (error) {
        if (error.code === "ENOENT") {
            console.log(`CSV file ${csvFilePath} not found. Skipping test generation for ${pageName}.`);
        } else {
            console.error(`Error reading or parsing CSV ${csvFilePath}: ${error.message}. Skipping test generation for ${pageName}.`);
        }
        // Create a skipping test file if CSV is missing or unreadable
        fs.writeFileSync(testFilePath, 
`// @ts-check
const { test, expect } = require("@playwright/test");

test.describe("${pageName} tests - (Data error)", () => {
    test("skip_due_to_data_error", async ({ page }) => {
        test.skip(true, "Skipping test as data CSV was missing or unreadable for this page.");
    });
});
`);
        return;
    }

    const pageUrl = elements[0].page_url;

    let testFileContent = 
`// @ts-check
const { test, expect } = require("@playwright/test");
const path = require("path");
const { loadCsvData, navigateToUrl, verifyLinkElement, verifyContentElement, logger } = require("${COMMON_MODULE_PATH}");

const PAGE_URL = "${pageUrl}";
const DATA_FILE = path.join(__dirname, "..", "data", "${path.basename(csvFilePath)}");

test.describe.configure({ mode: "parallel" }); // Enable parallel execution for tests within this file

test.describe("${pageName} page tests", () => {
    let pageElementsData;
    let sharedPage;

    test.beforeAll(async ({ browser }) => {
        logger.info("Running beforeAll hook for ${pageName}");
        pageElementsData = await loadCsvData(DATA_FILE);
        if (!pageElementsData || pageElementsData.length === 0) {
            logger.warn("No data loaded for ${pageName}, tests in this file might be skipped or fail.");
            // No need to create page if no data
            return;
        }
        sharedPage = await browser.newPage();
        const navigationSuccess = await navigateToUrl(sharedPage, PAGE_URL);
        if (!navigationSuccess) {
            logger.error("Failed to navigate in beforeAll for ${pageName}, subsequent tests may fail.");
            // Optionally, throw an error to stop tests if navigation is critical
            // throw new Error("Failed to navigate to page in beforeAll");
        }
    });

    test.afterAll(async () => {
        logger.info("Running afterAll hook for ${pageName}");
        if (sharedPage) {
            await sharedPage.close();
        }
    });

    if (!fs.existsSync(DATA_FILE) || fs.readFileSync(DATA_FILE, "utf-8").trim() === "") {
        test("data_file_empty_or_missing", async() => {
            logger.warn("Data file is empty or missing, skipping actual tests for ${pageName}.");
            test.skip(true, "Data file is empty or missing.");
        });
    } else {
`;

    elements.forEach((elementData, i) => {
        const elementType = elementData.element_type;
        const elementTextForName = String(elementData.text || "");
        const elementSelectorForName = String(elementData.selector_css || "");
        let baseName = elementTextForName.trim() || elementSelectorForName.trim() || `${elementType}_item_${i}`;
        const testName = sanitizeTestName(`${elementType}_${baseName}_${i}`);

        testFileContent += 
`        test("${testName}", async () => {
`;
        testFileContent += 
`            if (!sharedPage) test.skip(true, "Page setup failed in beforeAll or no data.");
`;
        testFileContent += 
`            if (!pageElementsData || pageElementsData.length === 0) test.skip(true, "No test data loaded.");
`;
        testFileContent += 
`            const currentElementData = pageElementsData[${i}];
`;
        testFileContent += 
`            if (!currentElementData) test.skip(true, "Element data not found for this test index.");
`;

        if (elementType === "link") {
            testFileContent += 
`            await verifyLinkElement(sharedPage, currentElementData, test);
`;
        } else if (elementType === "content") {
            testFileContent += 
`            await verifyContentElement(sharedPage, currentElementData, test);
`;
        } else {
            testFileContent += 
`            logger.warn("Unsupported element type: ${elementType} for selector ${elementData.selector_css}");
`;
            // Corrected line 153: Ensure the skip message is a single backticked string literal
            testFileContent += 
`            test.skip(true, 
              \	Unsupported element type: ${elementType}\
            );
`;
        }
        testFileContent += 
`        });

`;
    });

    testFileContent += 
`    }
});
`;

    fs.writeFileSync(testFilePath, testFileContent);
    console.log(`Generated JavaScript test file: ${testFilePath}`);
}

function main() {
    if (!fs.existsSync(TESTS_DIR)) {
        fs.mkdirSync(TESTS_DIR, { recursive: true });
    }
    // Clear existing test files
    fs.readdirSync(TESTS_DIR).forEach(file => {
        if (file.endsWith(".spec.js")) {
            fs.unlinkSync(path.join(TESTS_DIR, file));
            console.log(`Removed old test file: ${file}`);
        }
    });

    fs.readdirSync(DATA_DIR).forEach(fileName => {
        if (fileName.endsWith("_data.csv") && !fileName.endsWith("_archived_data.csv")) {
            const pageNameMatch = fileName.match(/(.+)_data\.csv/);
            if (pageNameMatch) {
                const pageName = pageNameMatch[1];
                const csvFilePath = path.join(DATA_DIR, fileName);
                generateJsTestFile(csvFilePath, pageName);
            }
        }
    });
}

main();

