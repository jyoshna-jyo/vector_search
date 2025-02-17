import pytest
from main import VectorDB

@pytest.fixture
def vector_db():
    return VectorDB(use_server=True, host="localhost", port=8000)

# Test Document Insertion
def test_insert_document(vector_db):
    vector_db.insert_document('1', 'Test document')
    results = vector_db.retrieve_documents('Test')
    assert 'Test document' in results

# Test Document Update
def test_update_document(vector_db):
    vector_db.insert_document('2', 'Old content')
    vector_db.update_document('2', 'New content')
    results = vector_db.retrieve_documents('New')
    assert 'New content' in results
    assert 'Old content' not in results

# Test Document Deletion
def test_delete_document(vector_db):
    vector_db.insert_document('3', 'Delete me')
    vector_db.delete_document('3')
    results = vector_db.retrieve_documents('Delete', top_n=1)
    assert 'Delete me' not in  results

# Test Edge Cases
def test_empty_document(vector_db):
    with pytest.raises(TypeError):
        vector_db.insert_document('4', None)

def test_non_existent_document(vector_db):
    results = vector_db.retrieve_documents('Nonexistent')
    assert 'Nonexistent' not in results