# Data Ingestion API System

This project implements a Data Ingestion API System using FastAPI. It provides RESTful APIs for submitting data ingestion requests and checking their status, with asynchronous processing and rate limiting.

## Project Structure

```
data-ingestion-api
├── app
│   ├── __init__.py
│   ├── main.py
│   ├── models.py
│   ├── services.py
│   ├── queue_manager.py
│   ├── store.py
│   └── config.py
├── tests
│   └── test_api.py
├── requirements.txt
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd data-ingestion-api
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

To run the application, execute the following command:
```
uvicorn app.main:app --reload
```

The API will be available at `http://127.0.0.1:8000`.

### Endpoints

- **POST /ingest**: Submit a data ingestion request.
  - Request Body:
    ```json
    {
      "ids": [1, 2, 3],
      "priority": "MEDIUM"
    }
    ```

- **GET /status/{ingestion_id}**: Check the status of a specific ingestion request.

## Testing

To run the tests, use the following command:
```
pytest tests/test_api.py
```

## Design Choices

- The application uses asynchronous processing to handle ingestion requests efficiently.
- A priority queue is implemented to manage the order of processing based on the priority of requests.
- Rate limiting is enforced to control the frequency of batch processing.

## License

This project is licensed under the MIT License.