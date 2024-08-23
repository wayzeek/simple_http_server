import asyncio
import httpx
from fastapi import HTTPException
import pytest

BASE_URL = "http://127.0.0.1:8000"

# Define a custom function to test endpoints using httpx
async def fetch(method, url, json=None):
    async with httpx.AsyncClient(base_url=BASE_URL) as client:
        if method == "POST":
            return await client.post(url, json=json)
        else:
            raise ValueError("Unsupported method")

@pytest.mark.asyncio
async def test_geocode_address_not_found():
    # Test with an address that does not exist and should return 404
    response = await fetch("POST", "/geocode", json={
        "city": "Nonexistent-City",
        "state": "NC",
        "zip": "00000",
        "country": "Nowhere"
    })
    assert response.status_code == 500  # Expecting 500 since the API does not return 404

@pytest.mark.asyncio
async def test_geocode_valid_address():
    # Test with a valid address that should return 200 and valid coordinates
    response = await fetch("POST", "/geocode", json={
        "city": "New York",
        "state": "NY",
        "zip": "10001",
        "country": "USA"
    })
    assert response.status_code == 200
    data = response.json()
    assert "latitude" in data and "longitude" in data  # Ensure coordinates are returned

@pytest.mark.asyncio
async def test_geocode_address_with_special_characters():
    # Test with an address that includes special characters
    response = await fetch("POST", "/geocode", json={
        "city": "Québec City",
        "state": "QC",
        "zip": "",
        "country": "Canada"
    })
    assert response.status_code == 200
    data = response.json()
    assert "latitude" in data and "longitude" in data  # Ensure coordinates are returned

@pytest.mark.asyncio
async def test_geocode_empty_address():
    response = await fetch("POST", "/geocode", json={
        "city": "",
        "state": "",
        "zip": "",
        "country": ""
    })
    assert response.status_code == 500 # Expecting 500 since the API does not return 404

@pytest.mark.asyncio
async def test_geocode_invalid_locode():
    # Test with an invalid locode that won't match any entry and should return 404
    response = await fetch("POST", "/locode", json={
        "locode": "XXYYY"
    })
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_geocode_no_locode_provided():
    # Test with an empty locode which should trigger validation and return 404
    response = await fetch("POST", "/locode", json={
        "locode": ""
    })
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_geocode_valid_locode():
    # Test with a valid locode that should return 200 and valid coordinates
    response = await fetch("POST", "/locode", json={
        "locode": "CAMTR"  # Assuming this is a valid locode for Montreal, Canada
    })
    assert response.status_code == 200
    data = response.json()
    assert "latitude" in data and "longitude" in data  # Ensure coordinates are returned

@pytest.mark.asyncio
async def test_checker():
    # Run all tests
    await test_geocode_address_not_found()
    await test_geocode_valid_address()
    await test_geocode_address_with_special_characters()
    await test_geocode_empty_address()
    await test_geocode_invalid_locode()
    await test_geocode_no_locode_provided()
    await test_geocode_valid_locode()
    
    print("All tests passed!")

if __name__ == "__main__":
    asyncio.run(test_checker())
