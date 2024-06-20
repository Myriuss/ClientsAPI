from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from main import app, get_db, Base, Client



# Override database URL for testing
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///./test_client.db"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

# Override get_db function for testing
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_create_client():
    response = client.post("/clients/", json={"name": "John Doe", "email": "john.doe@example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "John Doe"
    assert response.json()["email"] == "john.doe@example.com"
    assert "id" in response.json()

def test_read_client():
    # Assuming there's a client with id 1 in the test database
    response = client.get("/clients/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1

def test_update_client():
    # Assuming there's a client with id 1 in the test database
    response = client.put("/clients/1", json={"name": "Updated Name", "email": "updated.email@example.com"})
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Name"
    assert response.json()["email"] == "updated.email@example.com"

def test_delete_client():
    # Assuming there's a client with id 1 in the test database
    response = client.delete("/clients/1")
    assert response.status_code == 200
    assert response.json()["message"] == "Client deleted"
