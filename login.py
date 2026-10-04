from playwright.sync_api import sync_playwright
import requests
import time
from config import *

with sync_playwright() as p:
    # Launch browser (set headless=False to watch it happen)
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    
    # Go to the login page
    page.goto(revelUrl)
    
    # Wait for the JS inputs to render, then type credentials
    page.fill('input[name="username"]', revelUser)

    # Click the continue button
    page.click('button[type="submit"]')

    # Wait for password request
    page.fill('input[name="password"]', revelPassword)
    
    # Click the sign-in button
    page.click('button[type="submit"]')
    
    page.locator("#overview-payment-widget a:not([class])").filter(has_text="Yesterday").click()
    print("Successfully set yesterday")
    page.get_by_role("link", name="reports").click()
    page.wait_for_url(revelUrl+'/reports/sales_summary/')
    print("Successfully changed to reports")
    time.sleep(10)
    page.get_by_role("link", name="order history").click()
    page.wait_for_url(revelUrl+'/reports/orders/')
    print('Successfully changed to orders')
    time.sleep(10)
    page.locator("div.header-more").click()
    print('successfully open dropdown')
    time.sleep(10)
    with page.expect_download() as download_info:
        page.locator("ul.export-links > li").filter(has_text="csv").click()
    download = download_info.value
    destination_path = f"{downloadPath}{download.suggested_filename}"
    download.save_as(destination_path)
    time.sleep(30)
    
        
    # Keep the session alive or scrape data here
    browser.close()
