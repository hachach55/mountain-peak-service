from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from app.main import app
from app.database import Base, get_db   

# Use in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Override the get_db dependency for testing
def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

# Create tables in the test database
Base.metadata.create_all(bind=engine)

client = TestClient(app)

def test_create_peak():
    response = client.post(
        "/peaks/",
        json={"name": "Mount Everest", "latitude": 27.9881, "longitude": 86.9250, "altitude": 8848}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mount Everest"
    assert "id" in data

def test_read_peaks():
    # First, create a peak
    client.post(
        "/peaks/",
        json={"name": "K2", "latitude": 35.8825, "longitude": 76.5133, "altitude": 8611}
    )
    
    response = client.get("/peaks/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert any(peak["name"] == "K2" for peak in data)

def test_read_peak():
    # First, create a peak
    create_response = client.post(
        "/peaks/",
        json={"name": "Mont Blanc", "latitude": 45.833641, "longitude": 6.864594, "altitude": 4809}
    )
    peak_id = create_response.json()["id"]
    
    response = client.get(f"/peaks/{peak_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Mont Blanc"

def test_update_peak():
    # First, create a peak
    create_response = client.post(
        "/peaks/",
        json={"name": "Pic du Midi", "latitude": 42.9369, "longitude": 0.1411, "altitude": 2877}
    )
    peak_id = create_response.json()["id"]
    
    response = client.put(
        f"/peaks/{peak_id}",
        json={"name": "Pic du Midi Updated", "latitude": 27.9626, "longitude": 86.9336, "altitude": 8516}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pic du Midi Updated"

def test_delete_peak():
    # First, create a peak
    create_response = client.post(
        "/peaks/",
        json={"name": "Makalu", "latitude": 27.8897, "longitude": 87.0889, "altitude": 8485}
    )
    peak_id = create_response.json()["id"]
    
    response = client.delete(f"/peaks/{peak_id}")
    assert response.status_code == 200

    # Verify the peak is deleted
    get_response = client.get(f"/peaks/{peak_id}")
    assert get_response.status_code == 404

def test_search_peaks():

    db = TestingSessionLocal()
    db.query(Base.metadata.tables['peaks']).delete()
    db.commit()
    db.close()

    # Create some peaks
    client.post("/peaks/", json={"name": "Cho Oyu", "latitude": 28.0942, "longitude": 86.6608, "altitude": 8188})
    client.post("/peaks/", json={"name": "Dhaulagiri", "latitude": 28.6975, "longitude": 83.4872, "altitude": 8167})
    
    response = client.post(
        "/peaks/search/",
        json={"min_lat": 28, "max_lat": 29, "min_lon": 86, "max_lon": 87}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Cho Oyu"
