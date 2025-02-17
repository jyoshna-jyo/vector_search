# README for VectorDB with ChromaDB

## Introduction
This project implements a `VectorDB` class for CRUD operations on a vector database using ChromaDB. It supports document insertion, retrieval, updating, and deletion. The implementation allows running in either **local mode** or **server mode**.

## Prerequisites
- Python 3.10 or higher
- ChromaDB
- Uvicorn (for server mode)
- FastAPI (for server mode)
- Pytest (for testing)

## Installation
1. **Create a virtual environment (optional):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Mac or Linux 
   venv\\Scripts\\activate.bat # On Windows
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running ChromaDB Server (Optional)
If using server mode, start ChromaDB with:
```bash
chroma run --host 0.0.0.0 --port 8000
```

## Usage
### 1. Create a Collection and Insert Document
```bash
python main.py
```
This script will:
- Create a collection
- Read content from `sample.txt`
- Insert a document
- Update the document
- Retrieve results
- Delete the document

### 2. Sample `main.py`:
```python
# Run VectorDB operations
db = VectorDB(use_server=True, host="localhost", port=8000)
db.create_collection()
data = db.read_text_file('sample.txt')
db.insert_document('1', "".join(data))
db.update_document('1', "Updated vector mapping document.")
result = db.retrieve_documents("vector")
print(f"Retrieved: {result}")
db.delete_document('1')
```

### 3. Running Tests
Make sure that the venv is activated before this.

To run the unit tests with `pytest`:
```bash
pytest test_main.py --verbose
```

## Notes
- Adjust `use_server=True` or `use_server=False` depending on your setup.
- Ensure `sample.txt` exists with some sample text.
