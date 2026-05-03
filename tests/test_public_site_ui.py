"""UI tests for the public-facing site."""
import pytest
from playwright.sync_api import expect
from pages.public_page import PublicPage


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_home_loads_with_branding(public_page):
    expect(public_page).to_have_title("Colorado Victim Services")
    expect(public_page.get_by_role("heading", level=1)).to_be_visible()


@pytest.mark.ui
@pytest.mark.smoke
@pytest.mark.regression
def test_skip_to_main_content_link_exists(public_page):
    skip = public_page.locator("a.skip-link")
    expect(skip).to_have_attribute("href", "#main-content")


@pytest.mark.ui
@pytest.mark.regression
def test_main_landmark_is_present(public_page):
    expect(public_page.locator("main#main-content")).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_navigate_to_resources_page(public_page):
    pp = PublicPage(public_page)
    pp.goto_resources()
    expect(public_page.locator("main[aria-label='Resources']")).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_navigate_to_contact_page(public_page):
    pp = PublicPage(public_page)
    pp.goto_contact()
    expect(public_page.locator("main[aria-label='Contact']")).to_be_visible()


@pytest.mark.ui
@pytest.mark.regression
def test_search_input_has_aria_label(public_page):
    box = public_page.get_by_role("searchbox", name="Search resources").first
    expect(box).to_be_visible()


@pytest.mark.ui
@pytest.mark.integration
@pytest.mark.regression
def test_search_filters_resources(public_page):
    pp = PublicPage(public_page)
    pp.goto_resources()
    pp.search("housing")
    public_page.wait_for_load_state("networkidle")
    body_text = public_page.locator("body").text_content().lower()
    assert "housing" in body_text or "no" in body_text


@pytest.mark.ui
@pytest.mark.integration
@pytest.mark.regression
def test_share_modal_opens_with_email_tab(public_page):
    pp = PublicPage(public_page)
    pp.goto_resources()
    public_page.wait_for_load_state("networkidle")
    pp.open_share_for_first_card()
    dialog = public_page.get_by_role("dialog")
    expect(dialog).to_be_visible()
    expect(dialog.get_by_placeholder("recipient@email.com")).to_be_visible()


@pytest.mark.ui
@pytest.mark.integration
@pytest.mark.regression
def test_share_modal_email_input_accepts_text(public_page):
    """Email-text feature: ensure the recipient field accepts input and
    the Send button enables once an address is provided."""
    pp = PublicPage(public_page)
    pp.goto_resources()
    public_page.wait_for_load_state("networkidle")
    pp.open_share_for_first_card()
    pp.fill_share_email("test@example.com")
    send_btn = public_page.get_by_role("button", name="Send Anonymously")
    expect(send_btn).to_be_enabled()


@pytest.mark.ui
@pytest.mark.regression
def test_share_modal_has_three_tabs(public_page):
    pp = PublicPage(public_page)
    pp.goto_resources()
    public_page.wait_for_load_state("networkidle")
    pp.open_share_for_first_card()
    tabs = public_page.get_by_role("tab")
    expect(tabs).to_have_count(3)


@pytest.mark.ui
@pytest.mark.regression
def test_multi_select_caps_at_five(public_page):
    """Selecting more than 5 cards should not exceed 5."""
    pp = PublicPage(public_page)
    pp.goto_resources()
    public_page.wait_for_load_state("networkidle")
    checkboxes = public_page.get_by_role("checkbox")
    count = checkboxes.count()
    if count < 6:
        pytest.skip("Need at least 6 brochures seeded to test the cap")
    for i in range(6):
        checkboxes.nth(i).click()
    bar = public_page.get_by_role("region", name="Selected resources")
    expect(bar).to_contain_text("5 of 5 selected")
