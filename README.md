
# Geocoding API

This project is a FastAPI-based application that provides endpoints for geocoding addresses and locodes. It allows you to convert an address or locode into geographic coordinates (latitude and longitude) using an external geocoding service.

## Requirements

- Python 3.8+
- FastAPI
- Uvicorn
- httpx
- pytest
- pytest-asyncio
- dotenv

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/wayzeek/simple_http_server.git
   cd simple_http_server/
   ```

2. **Create and activate a virtual environment:**

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install the dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables:**

   Set up your Geocode API Key in the `.env` file in the root directory:

   ```
   API_KEY=your_geocoding_api_key
   ```

   Replace `your_geocoding_api_key` with your actual [API key](https://geocode.maps.co/join/).

## Running the Server

To start the FastAPI server, run the following command:

```bash
uvicorn app.main:app --reload
```

This will start the server at `http://127.0.0.1:8000`.

## API Endpoints

### 1. `/geocode` - Geocode an Address

- **Endpoint:** `POST /geocode`
- **Description:** Converts an address into geographic coordinates.
- **Request Body:**
  ```json
  {
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "USA"
  }
  ```
- **Response:**
  ```json
  {
    "latitude": 40.712776,
    "longitude": -74.005974
  }
  ```

- **Example `curl` request:**
  ```bash
  curl -X POST "http://127.0.0.1:8000/geocode"   -H "Content-Type: application/json"   -d '{
    "city": "New York",
    "state": "NY",
    "zip": "10001",
    "country": "USA"
  }'
  ```

### 2. `/locode` - Geocode a Locode

- **Endpoint:** `POST /locode`
- **Description:** Converts a locode into geographic coordinates by looking up the associated address first.
- **Request Body:**
  ```json
  {
    "locode": "CA MTR"
  }
  ```
- **Response:**
  ```json
  {
    "latitude": 45.5017,
    "longitude": -73.5673
  }
  ```

- **Example `curl` request:**
  ```bash
  curl -X POST "http://127.0.0.1:8000/locode"   -H "Content-Type: application/json"   -d '{
    "locode": "CA MTR"
  }'
  ```

## Running the Tests

To run the tests, including the ones that check the API endpoints for various scenarios, use the following command:

```bash
pytest app/test_errors.py
```

Make sure the server is running before executing the tests.
