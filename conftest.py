import os
import pytest
from dotenv import load_dotenv

load_dotenv(".env.test")


@pytest.fixture(scope="session")
def base_url():
    return os.getenv("BASE_URL", "http://localhost:5173")


@pytest.fixture(scope="session")
def supabase_url():
    url = os.getenv("SUPABASE_URL")
    if not url:
        pytest.skip("SUPABASE_URL not set in .env.test")
    return url


@pytest.fixture(scope="session")
def supabase_key():
    key = os.getenv("SUPABASE_ANON_KEY")
    if not key:
        pytest.skip("SUPABASE_ANON_KEY not set in .env.test")
    return key


@pytest.fixture(scope="session")
def admin_credentials():
    email = os.getenv("ADMIN_EMAIL")
    password = os.getenv("ADMIN_PASSWORD")
    if not email or not password:
        pytest.skip("ADMIN_EMAIL/ADMIN_PASSWORD not set in .env.test")
    return {"email": email, "password": password}


@pytest.fixture
def public_page(page, base_url):
    page.goto(base_url)
    return page


@pytest.fixture
def admin_page(page, base_url, admin_credentials):
    """Page logged in as admin. Admin route is base_url + '/admin' (path convention)."""
    page.goto(f"{base_url}/admin")
    page.get_by_placeholder("admin@covictims.org").fill(admin_credentials["email"])
    page.get_by_placeholder("••••••••").fill(admin_credentials["password"])
    page.get_by_role("button", name="Sign In").click()
    page.wait_for_load_state("networkidle")
    return page
