const fs = require("fs");
const { expect } = require("@playwright/test");

/**
 * Loads data from a CSV file and converts it to an array of objects.
 * Assumes the first row is the header.
 * @param {string} filePath - The path to the CSV file.
 * @returns {Array<Object>} An array of objects, where each object represents a row.
 */
function loadCsvData(filePath) {
    try {
        const fileContent = fs.readFileSync(filePath, "utf-8");
        const lines = fileContent.trim().split("\n");
        if (lines.length < 2) {
            console.error(`CSV file ${filePath} has no data rows.`);
            return [];
        }
        const headers = lines[0].split(",").map(header => header.trim());
        const data = [];
        for (let i = 1; i < lines.length; i++) {
            const values = lines[i].split(",").map(value => {
                let v = value.trim();
                if (v.startsWith('"') && v.endsWith('"')) {
                    v = v.substring(1, v.length - 1).replace(/""/g, '"');
                }
                return v;
            });
            if (values.length === headers.length) {
                const rowObject = {};
                headers.forEach((header, index) => {
                    rowObject[header] = values[index] === "" ? null : values[index]; // Handle empty strings as null for href if needed
                });
                data.push(rowObject);
            }
        }
        console.log(`Successfully loaded CSV data from ${filePath}`);
        return data;
    } catch (error) {
        console.error(`Error loading CSV ${filePath}: ${error.message}`);
        return [];
    }
}

/**
 * Navigates the Playwright page to the specified URL.
 * @param {import("@playwright/test").Page} page - The Playwright page object.
 * @param {string} url - The URL to navigate to.
 */
async function navigateToUrl(page, url) {
    try {
        console.log(`Navigating to URL: ${url}`);
        await page.goto(url, { waitUntil: "domcontentloaded", timeout: 30000 });
        await expect(page).toHaveURL(url, { timeout: 15000 });
        console.log(`Successfully navigated to ${url}`);
        return true;
    } catch (error) {
        console.error(`Failed to navigate to ${url}: ${error.message}`);
        throw error; // Re-throw to fail the test
    }
}

/**
 * Verifies a link element based on data from CSV.
 * @param {import("@playwright/test").Page} page - The Playwright page object.
 * @param {Object} elementData - An object containing element details (selector, text, href).
 */
async function verifyLinkElement(page, elementData) {
    const { selector, text: expectedText, href: expectedHref } = elementData;
    const pageUrl = page.url();
    console.log(`DEBUG: Raw selector from elementData for link: "${selector}"`); // DEBUG LOG ADDED
    console.log(`Verifying link on ${pageUrl} with selector "${selector}", expected text "${expectedText}", expected href "${expectedHref}"`);

    const linkElement = page.locator(selector).first();
    await linkElement.scrollIntoViewIfNeeded({ timeout: 5000 });
    await expect(linkElement).toBeVisible({ timeout: 10000 });

    // Verify text (if expectedText is provided and not for logo)
    if (expectedText && expectedText.toLowerCase() !== "plato logo") {
        const actualTextRaw = await linkElement.innerText();
        const actualText = actualTextRaw.trim().replace(/\s+/g, " ");
        expect(actualText, `Link text mismatch for selector "${selector}"`).toBe(expectedText.trim().replace(/\s+/g, " "));
        console.log(`Link text MATCH: Selector "${selector}"`);
    } else if (expectedText && expectedText.toLowerCase() === "plato logo") {
        const img = linkElement.locator("img").first();
        await expect(img).toHaveAttribute("alt", /plato/i, {timeout: 5000});
        console.log(`Logo image alt text verified for selector "${selector}"`);
    }

    // Verify href
    if (expectedHref) {
        const actualHref = await linkElement.getAttribute("href");
        expect(actualHref ? actualHref.trim().replace(/\/$/, "") : null, `Link href mismatch for selector "${selector}"`).toBe(expectedHref.trim().replace(/\/$/, ""));
        console.log(`Link href MATCH: Selector "${selector}"`);

        // Verify link accessibility by trying to navigate
        if (!expectedHref.startsWith("mailto:") && !expectedHref.startsWith("tel:") && !expectedHref.startsWith("#")) {
            let urlToCheck = actualHref;
            if (!urlToCheck.startsWith("http")) {
                const { URL } = require("url");
                urlToCheck = new URL(urlToCheck, page.url()).href;
            }
            console.log(`Checking accessibility of link: ${urlToCheck}`);
            const newPage = await page.context().newPage();
            try {
                const response = await newPage.goto(urlToCheck, { waitUntil: "domcontentloaded", timeout: 20000 });
                expect(response.status(), `Link ${urlToCheck} is broken or inaccessible.`).toBeLessThan(400);
                console.log(`Link ${urlToCheck} is accessible. Status: ${response.status()}`);
            } catch (e) {
                console.error(`Failed to access link ${urlToCheck}: ${e.message}`);
                // For 403s on specific URLs, we might log a warning instead of failing if that's desired
                // For now, let it fail as per strict checking
                throw new Error(`Failed to access link ${urlToCheck} (selector "${selector}"): ${e.message}`);
            } finally {
                await newPage.close();
            }
        }
    }
}

/**
 * Verifies a content element based on data from CSV.
 * @param {import("@playwright/test").Page} page - The Playwright page object.
 * @param {Object} elementData - An object containing element details (selector, text).
 */
async function verifyContentElement(page, elementData) {
    const { selector, text: expectedText } = elementData;
    const pageUrl = page.url();
    console.log(`Verifying content on ${pageUrl} with selector "${selector}", expected text "${expectedText}"`);

    const contentElement = page.locator(selector).first();
    await contentElement.scrollIntoViewIfNeeded({ timeout: 5000 });
    await expect(contentElement).toBeVisible({ timeout: 10000 });

    const actualTextRaw = await contentElement.innerText();
    const normalizedActualText = actualTextRaw.trim().replace(/\s+/g, " ");
    const normalizedExpectedText = expectedText.trim().replace(/\s+/g, " ");

    expect(normalizedActualText, `Content mismatch for selector "${selector}"`).toBe(normalizedExpectedText);
    console.log(`Content MATCH: Selector "${selector}"`);
}

module.exports = {
    loadCsvData,
    navigateToUrl,
    verifyLinkElement,
    verifyContentElement,
};

