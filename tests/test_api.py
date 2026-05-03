"""API tests against the Supabase REST endpoints used by the app."""
import pytest
import requests


def _headers(key):
    return {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Accept": "application/json",
    }


@pytest.mark.api
@pytest.mark.smoke
def test_categories_endpoint_returns_list(supabase_url, supabase_key):
    r = requests.get(
        f"{supabase_url}/rest/v1/categories?select=*",
        headers=_headers(supabase_key),
        timeout=10,
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)


@pytest.mark.api
@pytest.mark.smoke
def test_brochures_endpoint_returns_list(supabase_url, supabase_key):
    r = requests.get(
        f"{supabase_url}/rest/v1/brochures?select=*&limit=5",
        headers=_headers(supabase_key),
        timeout=10,
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert isinstance(data, list)


@pytest.mark.api
def test_brochure_shape_includes_expected_columns(supabase_url, supabase_key):
    r = requests.get(
        f"{supabase_url}/rest/v1/brochures?select=*&limit=1",
        headers=_headers(supabase_key),
        timeout=10,
    )
    assert r.status_code == 200
    rows = r.json()
    if not rows:
        pytest.skip("No brochures seeded")
    expected = {"id", "title", "category_id"}
    missing = expected - set(rows[0].keys())
    assert not missing, f"Missing columns: {missing}"


@pytest.mark.api
def test_anon_cannot_insert_brochure(supabase_url, supabase_key):
    """RLS: an anonymous request must NOT be able to insert."""
    r = requests.post(
        f"{supabase_url}/rest/v1/brochures",
        headers={**_headers(supabase_key), "Content-Type": "application/json"},
        json={"title": "anon-injection-attempt", "category_id": "test"},
        timeout=10,
    )
    # Either 401/403 (RLS denies) or 400 (constraint). 201 means RLS is broken.
    assert r.status_code != 201, "Anon insert succeeded — RLS misconfigured"


@pytest.mark.api
def test_phone_and_hours_columns_exist(supabase_url, supabase_key):
    """Verify the recent migration added phone_number and business_hours."""
    r = requests.get(
        f"{supabase_url}/rest/v1/brochures?select=phone_number,business_hours&limit=1",
        headers=_headers(supabase_key),
        timeout=10,
    )
    assert r.status_code == 200, \
        f"Columns missing — run the ALTER TABLE migration. Response: {r.text}"
