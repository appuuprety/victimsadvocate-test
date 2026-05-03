"""UI tests for the admin portal — covers add/edit/remove of brochures (banners)."""
import time
import pytest
from playwright.sync_api import expect
from pages.admin_page import AdminPage


def _unique_title(prefix="E2E Test Banner"):
    return f"{prefix} {int(time.time() * 1000)}"


@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.smoke
@pytest.mark.regression
def test_admin_login_lands_on_dashboard(admin_page):
    expect(admin_page.get_by_text("CVR Admin Portal")).to_be_visible()


@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.integration
@pytest.mark.regression
def test_add_brochure_appears_in_list(admin_page):
    """Add a new banner via the admin form, confirm it shows up."""
    ap = AdminPage(admin_page)
    title = _unique_title()

    ap.goto_brochures()
    ap.click_add_brochure()
    ap.fill_brochure_form(
        title=title,
        description="Created by automated Playwright test.",
        tags="test, e2e",
        link_url="https://example.org/test-resource",
        phone="(303) 555-0199",
        hours="Mon–Fri, 9am–5pm",
    )
    ap.submit_upload()

    admin_page.wait_for_load_state("networkidle")
    assert ap.brochure_exists(title), f"Brochure '{title}' did not appear after add"


@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.integration
@pytest.mark.regression
def test_add_then_remove_brochure(admin_page):
    """Full lifecycle: add a banner, then remove it."""
    ap = AdminPage(admin_page)
    title = _unique_title("E2E Lifecycle")

    # Add
    ap.goto_brochures()
    ap.click_add_brochure()
    ap.fill_brochure_form(
        title=title,
        description="Will be deleted.",
        link_url="https://example.org/lifecycle",
    )
    ap.submit_upload()
    admin_page.wait_for_load_state("networkidle")
    assert ap.brochure_exists(title), "Brochure missing after creation"

    # Remove
    ap.delete_brochure_by_title(title)
    admin_page.wait_for_load_state("networkidle")
    # Title should no longer be present
    assert not ap.brochure_exists(title, timeout=2000), \
        f"Brochure '{title}' still visible after delete"


@pytest.mark.ui
@pytest.mark.admin
@pytest.mark.regression
def test_admin_form_requires_title(admin_page):
    """Submitting the brochure form with no title should show an error."""
    ap = AdminPage(admin_page)
    ap.goto_brochures()
    ap.click_add_brochure()
    ap.submit_upload()
    expect(admin_page.get_by_text("Title is required.")).to_be_visible()
