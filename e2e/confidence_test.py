# Confidence tests, is basically tests to see the web-app looks sane.
from playwright.sync_api import Page, expect

def test_application_loads(page: Page):
    
    page.goto("http://localhost:8080")

    expect(page).to_have_title("Pastore")
