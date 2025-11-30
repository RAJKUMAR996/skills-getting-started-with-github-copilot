import uuid
import os
import sys

# Ensure src/ is importable
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from app import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_get_activities():
    res = client.get("/activities")
    assert res.status_code == 200
    data = res.json()
    assert isinstance(data, dict)
    # Known activity should exist
    assert "Chess Club" in data


def test_signup_and_unregister_cycle():
    activity = "Chess Club"
    email = f"test-{uuid.uuid4().hex}@example.com"

    # Ensure email not present yet
    before = client.get("/activities").json()
    assert email not in before[activity]["participants"]

    # Sign up
    signup = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert signup.status_code == 200
    assert "Signed up" in signup.json().get("message", "")

    # Check it's present
    after = client.get("/activities").json()
    assert email in after[activity]["participants"]

    # Unregister
    unreg = client.delete(f"/activities/{activity}/unregister", params={"email": email})
    assert unreg.status_code == 200
    assert "Unregistered" in unreg.json().get("message", "")

    # Ensure it's removed
    final = client.get("/activities").json()
    assert email not in final[activity]["participants"]
