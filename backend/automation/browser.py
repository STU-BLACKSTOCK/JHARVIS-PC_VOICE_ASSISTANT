from playwright.sync_api import sync_playwright

class BrowserAutomation:
    def __init__(self):
        self.playwright = None
        self.browser = None
        self.page = None

    def start(self):
        if not self.playwright:
            self.playwright = sync_playwright().start()
            # Launch edge or chrome. headless=False so user sees what's happening
            self.browser = self.playwright.chromium.launch(headless=False)
            self.page = self.browser.new_page()

    def stop(self):
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()
        self.playwright = None
        self.browser = None
        self.page = None

    def navigate(self, url: str):
        if not self.page: self.start()
        try:
            self.page.goto(url)
            return f"Navigated to {url}"
        except Exception as e:
            return f"Failed to navigate: {e}"

    def search_google(self, query: str):
        if not self.page: self.start()
        try:
            from urllib.parse import quote_plus
            url = f"https://www.google.com/search?q={quote_plus(query)}"
            self.page.goto(url)
            self.page.wait_for_load_state("networkidle")
            return f"Searched Google for '{query}'"
        except Exception as e:
            return f"Google search failed: {e}"

    def click_element(self, selector: str):
        if not self.page: return "Browser not started."
        try:
            self.page.click(selector)
            return f"Clicked element '{selector}'"
        except Exception as e:
            return f"Failed to click: {e}"

    def get_text_content(self, selector: str = "body"):
        if not self.page: return "Browser not started."
        try:
            return self.page.text_content(selector)
        except Exception as e:
            return f"Failed to get content: {e}"

browser_controller = BrowserAutomation()
