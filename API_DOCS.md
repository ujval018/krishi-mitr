# Krishi Mitr API Documentation

## Base URL
`http://localhost:5000`

## Authentication

### Register User
**Endpoint:** `POST /api/auth/register`

**Request Body:**
```json
{
    "username": "string (min 4 chars)",
    "password": "string (min 6 chars)"
}
```

**Success Response:**
```json
{
    "message": "User registered successfully"
}
```

**Error Responses:**
- 400: Invalid input (missing fields, short username/password)
- 400: User already exists

### Login User
**Endpoint:** `POST /api/auth/login`

**Request Body:**
```json
{
    "username": "string",
    "password": "string"
}
```

**Success Response:**
```json
{
    "message": "Login successful",
    "username": "string"
}
```

**Error Responses:**
- 400: Invalid input
- 401: Invalid credentials

## Crop Management

### Add Crop
**Endpoint:** `POST /api/crop/add`

**Request Body:**
```json
{
    "owner": "string",
    "name": "string",
    "type": "string ('barter' or 'resell')",
    "price": "number (required if type='resell')",
    "exchange_for": "string (required if type='barter')"
}
```

**Success Response:**
```json
{
    "message": "Crop added successfully!",
    "crop": {
        "id": "string (UUID)",
        "owner": "string",
        "name": "string",
        "type": "string",
        "price": "number|null",
        "exchange_for": "string|null"
    }
}
```

**Error Responses:**
- 400: Missing required fields
- 400: Invalid crop type
- 400: Missing price/exchange_for for type

### List Crops
**Endpoint:** `GET /api/crop/list`

**Success Response:**
```json
[
    {
        "id": "string",
        "owner": "string",
        "name": "string",
        "type": "string",
        "price": "number|null",
        "exchange_for": "string|null"
    }
]
```

### Barter Crop
**Endpoint:** `POST /api/crop/barter/:crop_id`

**Success Response:**
```json
{
    "message": "Crop bartered successfully!",
    "crop": {
        "id": "string",
        "owner": "string",
        "name": "string",
        "type": "string",
        "exchange_for": "string"
    }
}
```

**Error Responses:**
- 400: Invalid crop ID format
- 400: Crop not available for barter
- 404: Crop not found

### Buy Crop
**Endpoint:** `POST /api/crop/buy/:crop_id`

**Success Response:**
```json
{
    "message": "Crop purchased successfully!",
    "crop": {
        "id": "string",
        "owner": "string",
        "name": "string",
        "type": "string",
        "price": "number"
    }
}
```

**Error Responses:**
- 400: Invalid crop ID format
- 400: Crop not available for purchase
- 404: Crop not found
