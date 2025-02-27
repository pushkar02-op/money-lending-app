# tests/test_rbac.py
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import uuid
from fastapi.testclient import TestClient
from main import app  # Now that the project root is in the path, this should work.

client = TestClient(app)

def unique_email(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex}@example.com"

def register_user(name: str, email: str, password: str, role: str):
    return client.post(
        "/auth/register",
        json={
            "name": name,
            "email": email,
            "password": password,
            "role": role
        }
    )

def test_admin_dashboard_access():
    # Create an admin user with a unique email
    admin_email = unique_email("admin")
    admin_password = "admin123"
    response = register_user("Admin User", admin_email, admin_password, "admin")
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]

    # Access admin dashboard with admin token (should succeed)
    response = client.get(
        "/users/admin-dashboard", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    assert "admin" in response.json()["message"].lower()

def test_admin_dashboard_for_agent_fails():
    # Create an agent user with a unique email
    agent_email = unique_email("agent")
    agent_password = "agent123"
    response = register_user("Agent User", agent_email, agent_password, "agent")
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]

    # Access admin dashboard with agent token (should be forbidden)
    response = client.get(
        "/users/admin-dashboard", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403, response.text

def test_agent_dashboard_access():
    # Create an agent user with a unique email
    agent_email = unique_email("agent")
    agent_password = "agent123"
    response = register_user("Agent User 2", agent_email, agent_password, "agent")
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]

    # Access agent dashboard with agent token (should succeed)
    response = client.get(
        "/users/agent-dashboard", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200, response.text
    assert "agent" in response.json()["message"].lower()

def test_agent_dashboard_for_admin_fails():
    # Create an admin user with a unique email
    admin_email = unique_email("admin")
    admin_password = "admin123"
    response = register_user("Admin User 2", admin_email, admin_password, "admin")
    assert response.status_code == 200, response.text
    token = response.json()["access_token"]

    # Access agent dashboard with admin token (should be forbidden)
    response = client.get(
        "/users/agent-dashboard", 
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 403, response.text
