import os
import uuid

os.environ["DATABASE_URL"] = "sqlite:///./test_pocketsmart.db"
os.environ["SECRET_KEY"] = "test-secret"
os.environ["GEMINI_API_KEY"] = ""

from fastapi.testclient import TestClient

from app.main import app


def make_client():
    return TestClient(app)


def test_health():
    with make_client() as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_public_pages_render_without_template_error():
    with make_client() as client:
        for path in ["/", "/login", "/register"]:
            response = client.get(path)
            assert response.status_code == 200
            assert "PocketSmart AI" in response.text


def test_register_login_and_session():
    username = "tester_" + uuid.uuid4().hex[:10]
    email = username + "@example.com"

    with make_client() as client:
        response = client.post(
            "/register",
            json={
                "username": username,
                "email": email,
                "password": "StrongPass123",
                "confirm_password": "StrongPass123",
            },
        )
        assert response.status_code == 200

        response = client.post(
            "/login/form",
            data={"username": username, "password": "StrongPass123"},
            follow_redirects=False,
        )
        assert response.status_code == 303

        response = client.get("/api/session-info")
        assert response.status_code == 200
        assert response.json()["username"] == username


def login_test_user(client: TestClient):
    username = "planner_" + uuid.uuid4().hex[:10]
    client.post(
        "/register",
        json={
            "username": username,
            "email": username + "@example.com",
            "password": "StrongPass123",
            "confirm_password": "StrongPass123",
        },
    )
    response = client.post(
        "/login/form",
        data={"username": username, "password": "StrongPass123"},
        follow_redirects=False,
    )
    assert response.status_code == 303


def test_home_party_jewelry_fallbacks_work_without_gemini():
    with make_client() as client:
        login_test_user(client)

        home = client.post(
            "/api/generate-home",
            json={
                "total_budget": 50000,
                "rooms": ["Living Room"],
                "num_lights": 4,
                "num_fans": 2,
                "num_furniture": 2,
                "num_dining_tables": 1,
                "style": "modern",
                "additional_requirements": "",
            },
        )
        assert home.status_code == 200
        assert home.json()["result"]["total_budget"] == 50000.0
        assert home.json()["result"]["estimated_total"] <= 50000

        party = client.post(
            "/api/generate-party",
            json={
                "total_budget": 30000,
                "num_guests": 20,
                "party_type": "Birthday",
                "venue_type": "hall",
                "needs": ["Catering", "Decoration"],
                "additional_requirements": "",
            },
        )
        assert party.status_code == 200
        assert party.json()["result"]["estimated_total"] <= 30000

        jewelry = client.post(
            "/api/generate-jewelry",
            data={
                "total_budget": "10000",
                "occasion": "Wedding",
                "style": "classic",
                "preferences": "gold tone",
            },
        )
        assert jewelry.status_code == 200
        assert jewelry.json()["result"]["estimated_total"] <= 10000

        history = client.get("/api/history")
        assert history.status_code == 200
        assert len(history.json()) >= 3
