import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database.database import Base, get_db
from core.config import settings
from main import app

# Create a test database URL - this is just used for connection
# but we won't actually create test-specific tables
# We'll connect to the same database
TEST_DATABASE_URL = settings.DATABASE_URL

# Create test engine - connects to the same database
test_engine = create_engine(TEST_DATABASE_URL)

# Create test session
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(scope="session")
def db_session():
    """
    Creates a test session that doesn't affect the real database tables
    """
    # Setting TESTING to True prevents table creation/modification
    settings.TESTING = True
    
    # Connect to the existing database
    connection = test_engine.connect()
    
    # Begin a nested transaction that will be rolled back after tests
    transaction = connection.begin()
    
    # Create a session bound to the connection
    session = TestingSessionLocal(bind=connection)
    
    try:
        yield session
    finally:
        # Make sure we roll back the transaction after the test
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture
def client(db_session):
    """
    Create a test client with a database session dependency override
    """
    # Override the get_db dependency to use our test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    # Clear the dependency override after the test
    app.dependency_overrides.clear()
