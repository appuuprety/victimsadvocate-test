"""Page object for the admin portal."""


class AdminPage:
    def __init__(self, page):
        self.page = page

    # ── navigation ──────────────────────────────────────────
    def goto_brochures(self):
        self.page.get_by_role("button", name="Brochures").click()

    # ── add brochure ────────────────────────────────────────
    def click_add_brochure(self):
        self.page.get_by_role("button", name="+ Add Brochure").first.click()

    def fill_brochure_form(self, title, description="", tags="", link_url="",
                           phone="", hours=""):
        self.page.get_by_placeholder("Brochure title…").fill(title)
        if description:
            self.page.get_by_placeholder(
                "Brief description of what this resource covers…"
            ).fill(description)
        if tags:
            self.page.get_by_placeholder("housing, shelter, emergency").fill(tags)
        if link_url:
            self.page.get_by_placeholder("https://example.gov/resource.pdf").fill(link_url)
        if phone:
            self.page.get_by_placeholder("(303) 555-0100").fill(phone)
        if hours:
            self.page.get_by_placeholder("Mon–Fri, 8am–5pm").fill(hours)

    def submit_upload(self):
        self.page.get_by_role("button", name="Upload Brochure").click()

    def submit_save_changes(self):
        self.page.get_by_role("button", name="Save Changes").click()

    # ── delete ──────────────────────────────────────────────
    def delete_brochure_by_title(self, title):
        # Native confirm() must be auto-accepted
        self.page.once("dialog", lambda d: d.accept())
        # Find the card with this title and click its Delete button
        card = self.page.locator(f"text={title}").first.locator(
            "xpath=ancestor::*[self::div][1]"
        )
        card.get_by_role("button", name="Delete").click()

    def brochure_exists(self, title, timeout=5000):
        try:
            self.page.wait_for_selector(f"text={title}", timeout=timeout)
            return True
        except Exception:
            return False
