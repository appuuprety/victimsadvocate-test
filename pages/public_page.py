"""Page object for the public-facing portal."""


class PublicPage:
    def __init__(self, page):
        self.page = page

    # ── navigation ──────────────────────────────────────────
    def goto_home(self, base_url):
        self.page.goto(base_url)

    def goto_resources(self):
        # Click the "Resources" nav button (icon + label)
        self.page.get_by_role("button", name="Resources").first.click()

    def goto_contact(self):
        self.page.get_by_role("button", name="Contact").first.click()

    # ── search ──────────────────────────────────────────────
    def search(self, query):
        box = self.page.get_by_role("searchbox", name="Search resources").first
        box.fill(query)
        box.press("Enter")

    # ── share modal ─────────────────────────────────────────
    def open_share_for_first_card(self):
        self.page.get_by_role("button", name="Share", exact=False).first.click()

    def share_modal_title(self):
        return self.page.get_by_role("dialog").locator("h3").first.text_content()

    def fill_share_email(self, email):
        self.page.get_by_placeholder("recipient@email.com").fill(email)

    def click_send_anonymously(self):
        self.page.get_by_role("button", name="Send Anonymously").click()

    # ── multi-select ────────────────────────────────────────
    def select_first_n_cards(self, n):
        checkboxes = self.page.get_by_role("checkbox")
        for i in range(n):
            checkboxes.nth(i).click()

    def selection_bar_text(self):
        return self.page.get_by_role("region", name="Selected resources").text_content()

    def click_share_selected(self):
        self.page.get_by_role("button", name="Share", exact=False).filter(
            has_text="Resource"
        ).first.click()
