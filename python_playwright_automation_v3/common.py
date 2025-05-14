import pandas as pd
import logging
import os
from playwright.sync_api import Page, expect
import pytest # Ensure pytest is imported if used directly for fail
from urllib.parse import urljoin # Ensure urljoin is imported

# Setup logging
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    filename=
                    "logs/automation_python.log",
                    filemode=
                    "w") 
logger = logging.getLogger(__name__)

def load_csv_data(csv_path):
    """Loads data from a CSV file."""
    try:
        df = pd.read_csv(csv_path)
        logger.info(f"Successfully loaded CSV data from {csv_path}")
        df = df.fillna("")
        return df.to_dict("records")
    except FileNotFoundError:
        logger.error(f"CSV file not found: {csv_path}")
        return []
    except Exception as e:
        logger.error(f"Error loading CSV {csv_path}: {e}")
        return []

def navigate_to_url(page: Page, url: str):
    """Navigates the Playwright page to the specified URL."""
    try:
        logger.info(f"Navigating to URL: {url}")
        page.goto(url, wait_until="domcontentloaded", timeout=30000) 
        expect(page).to_have_url(url, timeout=15000)
        logger.info(f"Successfully navigated to {url}")
        return True
    except Exception as e:
        logger.error(f"Failed to navigate to {url}: {e}")
        return False

def verify_link_element(page: Page, element_data: dict):
    """Verifies a link element based on data from CSV."""
    selector = element_data.get("selector") 
    expected_text = str(element_data.get("text", "")).strip()
    expected_href = str(element_data.get("href", "")).strip()
    page_url = page.url 

    logger.info(f"Verifying link on {page_url} with selector 	'{selector}	', expected text 	'{expected_text}	', expected href 	'{expected_href}	'")

    try:
        link_element = page.locator(selector).first
        link_element.scroll_into_view_if_needed(timeout=5000)
        expect(link_element).to_be_visible(timeout=10000)
        
        actual_text_raw = link_element.inner_text()
        actual_text = " ".join(actual_text_raw.split()).strip() 
        
        if expected_text.lower() == "plato logo":
            img_alt = link_element.locator("img").first.get_attribute("alt")
            if img_alt and "plato" in img_alt.lower():
                logger.info(f"Logo image found with alt text: 	'{img_alt}	'")
                actual_text = expected_text 
            else:
                logger.warning(f"Logo image alt text mismatch or not found. Expected part: 	'plato logo'	, Alt: 	'{img_alt}	'")
        elif expected_text: 
            if actual_text == expected_text:
                logger.info(f"Link text MATCH: Selector 	'{selector}	', Expected: 	'{expected_text}	', Actual: 	'{actual_text}	'")
            else:
                logger.error(f"Link text MISMATCH: Selector 	'{selector}	', Expected: 	'{expected_text}	', Actual: 	'{actual_text}	'")
                pytest.fail(f"Link text MISMATCH for {selector}. Expected: 	'{expected_text}	', Got: 	'{actual_text}	'")

        actual_href = link_element.get_attribute("href")
        if actual_href:
            actual_href = actual_href.strip()
            normalized_actual_href = actual_href.rstrip("/")
            normalized_expected_href = expected_href.rstrip("/")
            if normalized_actual_href == normalized_expected_href:
                logger.info(f"Link href MATCH: Selector 	'{selector}	', Expected: 	'{expected_href}	', Actual: 	'{actual_href}	'")
            else:
                logger.error(f"Link href MISMATCH: Selector 	'{selector}	', Expected: 	'{expected_href}	', Actual: 	'{actual_href}	'")
                pytest.fail(f"Link href MISMATCH for {selector}. Expected: 	'{expected_href}	', Got: 	'{actual_href}	'")
        elif expected_href: 
             logger.error(f"Link href MISSING: Selector 	'{selector}	', Expected: 	'{expected_href}	', but no href attribute found.")
             pytest.fail(f"Link href MISSING for {selector}. Expected: {expected_href}")

        # Link accessibility check using Playwright navigation
        if expected_href and not expected_href.startswith("mailto:") and not expected_href.startswith("tel:") and not expected_href.startswith("#"):
            url_to_check = actual_href if actual_href else expected_href
            if not url_to_check.startswith("http"):
                url_to_check = urljoin(page.url, url_to_check)
            
            logger.info(f"Attempting Playwright navigation to check link accessibility: {url_to_check}")
            new_page = None
            try:
                new_page = page.context.new_page()
                response = new_page.goto(url_to_check, wait_until="domcontentloaded", timeout=20000)
                if response:
                    status = response.status
                    logger.info(f"Playwright navigation to {url_to_check} successful. Status: {status}")
                    if status >= 400:
                        logger.error(f"Link {url_to_check} (selector '{selector}') is broken. Status code: {status}")
                        pytest.fail(f"Link {url_to_check} is broken. Status: {status}")
                else:
                    # This case should ideally not happen if goto doesn't throw and returns None, but good to log
                    logger.error(f"Playwright navigation to {url_to_check} (selector '{selector}') returned no response object.")
                    pytest.fail(f"Link {url_to_check} (selector '{selector}') returned no response.")
            except Exception as pw_e:
                logger.error(f"Playwright navigation to {url_to_check} (selector '{selector}') failed: {pw_e}")
                pytest.fail(f"Link {url_to_check} (selector '{selector}') failed during Playwright navigation: {pw_e}")
            finally:
                if new_page:
                    new_page.close()
        return True

    except Exception as e:
        logger.error(f"Error verifying link with selector 	'{selector}	': {e}")
        pytest.fail(f"Error verifying link {selector}: {e}")
        return False

def verify_content_element(page: Page, element_data: dict):
    """Verifies a content element based on data from CSV."""
    selector = element_data.get("selector") 
    expected_text = str(element_data.get("text", "")).strip()
    page_url = page.url 

    logger.info(f"Verifying content on {page_url} with selector 	'{selector}	', expected text 	'{expected_text}	'")

    try:
        content_element = page.locator(selector).first
        content_element.scroll_into_view_if_needed(timeout=5000)
        expect(content_element).to_be_visible(timeout=10000)
        
        actual_text_raw = content_element.inner_text()
        normalized_actual_text = " ".join(actual_text_raw.split()).strip()
        normalized_expected_text = " ".join(expected_text.split()).strip()

        if normalized_actual_text == normalized_expected_text:
            logger.info(f"Content MATCH: Selector 	'{selector}	', Expected: 	'{normalized_expected_text}	', Actual: 	'{normalized_actual_text}	'")
        else:
            logger.error(f"Content MISMATCH: Selector 	'{selector}	'. Expected: 	'{normalized_expected_text}	', Actual: 	'{normalized_actual_text}	'")
            pytest.fail(f"Content MISMATCH for {selector}. Expected: 	'{normalized_expected_text}	', Got: 	'{normalized_actual_text}	'")
        return True
            
    except Exception as e:
        logger.error(f"Error verifying content with selector 	'{selector}	': {e}")
        pytest.fail(f"Error verifying content {selector}: {e}")
        return False

