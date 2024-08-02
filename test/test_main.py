import pytest
from test.test_database import client
from app.database.connection import SessionLocal, engine, Base

@pytest.fixture(scope="module")
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def created_short_url(setup_db):
    url = "https://example.com"
    response = client.post("/shorten", json={"url": url, "expires_at": "0"})
    assert response.status_code == 200
    data = response.json()
    assert "short_url" in data
    return data["short_url"]

def test_create_url(created_short_url):
    assert created_short_url.startswith("http://localhost:8000/")

def test_redirect_to_url(created_short_url):
    short_key = created_short_url.split("/")[-1]
    print('test_redirect_to_url :',short_key)
    redirect_response = client.get(f"/{short_key}", follow_redirects=False)
    
    assert redirect_response.status_code == 301
    assert redirect_response.headers["location"] == "https://example.com"

def test_nonexistent_url():
    response = client.get("/none", follow_redirects=False)
    assert response.status_code == 404   
    
def test_get_statistics(created_short_url):
    short_key = created_short_url.split("/")[-1]

    initial_stats = client.get(f"/stats/{short_key}")
    assert initial_stats.status_code == 200
    stats_data = initial_stats.json()
    assert stats_data['visit_count'] == 0
    assert stats_data['last_visited'] is None

    client.get(f"/{short_key}", follow_redirects=False)

    updated_stats = client.get(f"/stats/{short_key}")
    assert updated_stats.status_code == 200
    stats_data = updated_stats.json()
    assert stats_data['visit_count'] == 1
    assert stats_data['last_visited'] is not None

def test_nonexistent_url_statistics():
    response = client.get("/stats/none")
    assert response.status_code == 404

# 여러번 접속을 가정한 테스트
def test_multiple_visits(created_short_url):
    short_key = created_short_url.split("/")[-1]

    for _ in range(3):
        client.get(f"/{short_key}", follow_redirects=False)

    stats = client.get(f"/stats/{short_key}")
    assert stats.status_code == 200
    stats_data = stats.json()
    assert stats_data['visit_count'] == 3
