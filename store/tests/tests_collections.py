from core.models import User  # Use the same User model as conftest
from store.models import Collection
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery import baker
import pytest

@pytest.fixture 
def create_collection(api_client):
    def do_create_collection(data):  # Changed parameter name for clarity
        return api_client.post("/store/collections/", data)
    return do_create_collection

@pytest.mark.django_db
class TestCreateCollections:  
    def test_if_user_is_anonymous(self, api_client, create_collection):
        # Arrange & Act
        response = create_collection({'title': 'a'})  # Fixed: pass dict directly
        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_if_user_is_not_admin_403(self, api_client, authenticate, create_collection):
        # Arrange & Act
        authenticate(is_staff=False)  # Fixed: added authenticate fixture and passed it
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_if_data_is_invalid_400(self, authenticate, create_collection):
        # Arrange & Act
        authenticate(is_staff=True)  # Use authenticate fixture for consistency
        response = create_collection({'title': ''})
        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert response.data['title'] is not None
    
    def test_if_data_is_valid_201(self, authenticate, create_collection):
        # Arrange & Act
        authenticate(is_staff=True)  # Use authenticate fixture for consistency
        response = create_collection({'title': 'a'})
        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['id'] > 0

@pytest.mark.django_db
class TestRetrieveCollections:
    def test_if_collection_exists_returns_200(self, api_client):
        # Create a single collection
        collection = baker.make(Collection)
        
        # Retrieve it
        response = api_client.get(f"/store/collections/{collection.id}/")
        
        # Assert
        assert response.status_code == status.HTTP_200_OK
        assert response.data == {
            "id": collection.id,
            "title": collection.title,
            "product_count": 0
        }