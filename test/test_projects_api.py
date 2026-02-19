"""
Tests for the projects CRUD API
"""
import sys
import os
import importlib.util

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database.models import Base


def _load_projects_module():
    """Load projects.py directly to avoid triggering api/routes/__init__.py."""
    spec = importlib.util.spec_from_file_location(
        "projects_route",
        os.path.join(os.path.dirname(__file__), '..', 'backend', 'api', 'routes', 'projects.py'),
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture(scope="module")
def client():
    """Create a TestClient with an in-memory SQLite database."""
    # Patch settings before loading the module
    from config.settings import settings as _settings
    original_url = _settings.DATABASE_URL
    _settings.DATABASE_URL = "sqlite://"

    projects_module = _load_projects_module()
    router = projects_module.router
    get_db = projects_module.get_db

    # Replace module-level engine with a shared in-memory engine using StaticPool
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=test_engine)
    TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    # Also patch the module so its own code (if it bypasses get_db) uses the same engine
    projects_module.engine = test_engine
    projects_module.SessionLocal = TestSessionLocal

    def override_get_db():
        db = TestSessionLocal()
        try:
            yield db
        finally:
            db.close()

    from fastapi import FastAPI
    app = FastAPI()
    app.include_router(router)
    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as c:
        yield c

    _settings.DATABASE_URL = original_url


def test_create_project(client):
    response = client.post("/projects", json={
        "title": "Test Novel",
        "description": "A test description",
        "genre": "Fantasy",
        "status": "draft",
        "content": "Once upon a time"
    })
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Novel"
    assert data["status"] == "draft"
    assert "id" in data


def test_list_projects(client):
    response = client.get("/projects")
    assert response.status_code == 200
    projects = response.json()
    assert isinstance(projects, list)
    assert len(projects) >= 1


def test_get_project_by_id(client):
    # First create a project
    create_resp = client.post("/projects", json={"title": "GetById", "status": "draft"})
    assert create_resp.status_code == 201
    project_id = create_resp.json()["id"]

    response = client.get(f"/projects/{project_id}")
    assert response.status_code == 200
    assert response.json()["id"] == project_id
    assert response.json()["title"] == "GetById"


def test_get_project_not_found(client):
    response = client.get("/projects/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_update_project(client):
    create_resp = client.post("/projects", json={"title": "Original", "status": "draft"})
    assert create_resp.status_code == 201
    project_id = create_resp.json()["id"]

    update_resp = client.put(f"/projects/{project_id}", json={"title": "Updated", "status": "published"})
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["title"] == "Updated"
    assert data["status"] == "published"


def test_delete_project(client):
    create_resp = client.post("/projects", json={"title": "ToDelete", "status": "draft"})
    assert create_resp.status_code == 201
    project_id = create_resp.json()["id"]

    delete_resp = client.delete(f"/projects/{project_id}")
    assert delete_resp.status_code == 204

    get_resp = client.get(f"/projects/{project_id}")
    assert get_resp.status_code == 404


def test_list_projects_with_status_filter(client):
    client.post("/projects", json={"title": "Draft1", "status": "draft"})
    client.post("/projects", json={"title": "Archived1", "status": "archived"})

    draft_resp = client.get("/projects?status=draft")
    assert draft_resp.status_code == 200
    for p in draft_resp.json():
        assert p["status"] == "draft"

    archived_resp = client.get("/projects?status=archived")
    assert archived_resp.status_code == 200
    for p in archived_resp.json():
        assert p["status"] == "archived"
