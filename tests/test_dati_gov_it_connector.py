from opengovsec.connectors.dati_gov_it import build_package_search_url


def test_build_package_search_url_encodes_query():
    url = build_package_search_url("ambiente urbano", limit=20, offset=5)
    assert "package_search" in url
    assert "ambiente+urbano" in url
    assert "rows=20" in url
    assert "start=5" in url


def test_build_package_search_url_limits_rows_to_100():
    url = build_package_search_url("ambiente", limit=500)
    assert "rows=100" in url
