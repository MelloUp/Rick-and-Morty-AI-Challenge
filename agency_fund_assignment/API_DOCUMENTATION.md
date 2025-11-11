# API Documentation

Complete API reference for the Rick & Morty AI Challenge application.

## Base URL

```
http://localhost:5000/api
```

## Response Format

All API responses follow this format:

```json
{
  "success": true|false,
  "data": {...} | [...],
  "error": "error message" (only if success is false)
}
```

---

## Locations API

### Get All Locations

Retrieve all locations from the Rick & Morty universe.

**Endpoint**: `GET /api/locations`

**Query Parameters**:
- `include_residents` (boolean, optional): Include full resident details. Default: false

**Example Request**:
```bash
curl http://localhost:5000/api/locations?include_residents=true
```

**Example Response**:
```json
{
  "success": true,
  "count": 126,
  "data": [
    {
      "id": 1,
      "name": "Earth (C-137)",
      "type": "Planet",
      "dimension": "Dimension C-137",
      "residents": ["https://rickandmortyapi.com/api/character/38", ...],
      "residents_details": [
        {
          "id": 38,
          "name": "Beth Smith",
          "status": "Alive",
          "species": "Human",
          "image": "https://rickandmortyapi.com/api/character/avatar/38.jpeg"
        }
      ]
    }
  ]
}
```

### Get Specific Location

Get details for a specific location by ID.

**Endpoint**: `GET /api/locations/<id>`

**Example Request**:
```bash
curl http://localhost:5000/api/locations/1
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "id": 1,
    "name": "Earth (C-137)",
    "type": "Planet",
    "dimension": "Dimension C-137",
    "residents_details": [...]
  }
}
```

**Error Response** (404):
```json
{
  "success": false,
  "error": "404 Client Error: Not Found"
}
```

---

## Characters API

### Get Character Details

Get detailed information about a specific character.

**Endpoint**: `GET /api/characters/<id>`

**Example Request**:
```bash
curl http://localhost:5000/api/characters/1
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "character": {
      "id": 1,
      "name": "Rick Sanchez",
      "status": "Alive",
      "species": "Human",
      "type": "",
      "gender": "Male",
      "origin": {
        "name": "Earth (C-137)",
        "url": "https://rickandmortyapi.com/api/location/1"
      },
      "location": {
        "name": "Citadel of Ricks",
        "url": "https://rickandmortyapi.com/api/location/3"
      },
      "image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg",
      "episode": [...]
    },
    "notes": [
      {
        "id": 1,
        "character_id": 1,
        "character_name": "Rick Sanchez",
        "note": "Genius scientist with portal gun technology",
        "created_at": "2024-01-15T10:30:00",
        "updated_at": "2024-01-15T10:30:00"
      }
    ]
  }
}
```

### Search Characters

Search for characters by name.

**Endpoint**: `GET /api/characters/search`

**Query Parameters**:
- `name` (string, required): Character name to search for

**Example Request**:
```bash
curl "http://localhost:5000/api/characters/search?name=Rick"
```

**Example Response**:
```json
{
  "success": true,
  "count": 89,
  "data": [
    {
      "id": 1,
      "name": "Rick Sanchez",
      "status": "Alive",
      "species": "Human",
      "gender": "Male",
      "image": "https://rickandmortyapi.com/api/character/avatar/1.jpeg"
    }
  ]
}
```

**Error Response** (400):
```json
{
  "success": false,
  "error": "Name parameter is required"
}
```

---

## Notes API

### Add Note

Add a note for a character.

**Endpoint**: `POST /api/notes`

**Request Body**:
```json
{
  "character_id": 1,
  "character_name": "Rick Sanchez",
  "note": "Invented the portal gun in his garage"
}
```

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{"character_id": 1, "character_name": "Rick Sanchez", "note": "Genius inventor"}'
```

**Example Response** (201):
```json
{
  "success": true,
  "note_id": 5
}
```

### Get Notes for Character

Get all notes for a specific character.

**Endpoint**: `GET /api/notes/<character_id>`

**Example Request**:
```bash
curl http://localhost:5000/api/notes/1
```

**Example Response**:
```json
{
  "success": true,
  "count": 2,
  "data": [
    {
      "id": 1,
      "character_id": 1,
      "character_name": "Rick Sanchez",
      "note": "First note about Rick",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### Update Note

Update an existing note.

**Endpoint**: `PUT /api/notes/<note_id>`

**Request Body**:
```json
{
  "note": "Updated note content"
}
```

**Example Request**:
```bash
curl -X PUT http://localhost:5000/api/notes/1 \
  -H "Content-Type: application/json" \
  -d '{"note": "Updated note content"}'
```

**Example Response**:
```json
{
  "success": true
}
```

### Delete Note

Delete a note.

**Endpoint**: `DELETE /api/notes/<note_id>`

**Example Request**:
```bash
curl -X DELETE http://localhost:5000/api/notes/1
```

**Example Response**:
```json
{
  "success": true
}
```

---

## AI Features API

### Generate Location Summary

Generate a Rick & Morty style summary for a location.

**Endpoint**: `GET /api/ai/location-summary/<location_id>`

**Example Request**:
```bash
curl http://localhost:5000/api/ai/location-summary/1
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "location": {
      "id": 1,
      "name": "Earth (C-137)",
      "type": "Planet",
      "dimension": "Dimension C-137"
    },
    "summary": "Ah yes, Earth C-137, the dimension where everything went sideways because one alcoholic genius couldn't keep his portal gun in his pants. A planet crawling with humans who have no idea they're living in one of infinite timelines where their choices don't really matter—existential dread sold separately."
  }
}
```

### Generate Character Dialogue

Generate a conversation between two characters.

**Endpoint**: `POST /api/ai/character-dialogue`

**Request Body**:
```json
{
  "character1_id": 1,
  "character2_id": 2
}
```

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/ai/character-dialogue \
  -H "Content-Type: application/json" \
  -d '{"character1_id": 1, "character2_id": 2}'
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "character1": {...},
    "character2": {...},
    "dialogue": "Rick: Morty, we need to *burp* go on an adventure.\nMorty: Oh geez Rick, I don't know about this...\nRick: Don't be such a wuss, Morty. It'll be fun!\nMorty: Your definition of fun usually involves near-death experiences!"
  }
}
```

### Generate Character Analysis

Get an AI-powered analysis of a character.

**Endpoint**: `GET /api/ai/character-analysis/<character_id>`

**Example Request**:
```bash
curl http://localhost:5000/api/ai/character-analysis/1
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "character": {...},
    "analysis": "Rick Sanchez is the quintessential mad scientist—brilliant, nihilistic, and deeply flawed. His genius-level intellect and mastery of interdimensional travel come packaged with severe alcoholism and emotional detachment, creating a character who's simultaneously the family's greatest asset and biggest liability."
  }
}
```

---

## Semantic Search API

### Index Characters

Generate and store embeddings for characters to enable semantic search.

**Endpoint**: `POST /api/search/index-characters`

**Request Body** (optional):
```json
{
  "character_ids": [1, 2, 3, 4, 5]
}
```

If no character_ids provided, indexes first 50 characters by default.

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/search/index-characters \
  -H "Content-Type: application/json" \
  -d '{}'
```

**Example Response**:
```json
{
  "success": true,
  "indexed_count": 50,
  "errors": []
}
```

### Semantic Search

Search characters using natural language queries.

**Endpoint**: `POST /api/search/semantic`

**Request Body**:
```json
{
  "query": "genius scientists from Earth",
  "top_k": 5
}
```

**Parameters**:
- `query` (string, required): Natural language search query
- `top_k` (integer, optional): Number of results to return. Default: 5

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/search/semantic \
  -H "Content-Type: application/json" \
  -d '{"query": "genius scientists", "top_k": 3}'
```

**Example Response**:
```json
{
  "success": true,
  "query": "genius scientists",
  "count": 3,
  "data": [
    {
      "character_id": 1,
      "character_name": "Rick Sanchez",
      "similarity": 0.8745,
      "metadata": {
        "species": "Human",
        "status": "Alive"
      },
      "character": {
        "id": 1,
        "name": "Rick Sanchez",
        "status": "Alive",
        "species": "Human",
        "image": "..."
      }
    }
  ]
}
```

---

## Evaluation API

### Evaluate Factual Consistency

Evaluate if generated text is factually consistent with source data.

**Endpoint**: `POST /api/eval/factual-consistency`

**Request Body**:
```json
{
  "generated_text": "Rick is a scientist who invented the portal gun",
  "source_data": {
    "name": "Rick Sanchez",
    "species": "Human",
    "occupation": "Scientist"
  }
}
```

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/eval/factual-consistency \
  -H "Content-Type: application/json" \
  -d '{"generated_text": "Rick is a scientist", "source_data": {"name": "Rick Sanchez"}}'
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "score": 8,
    "raw_response": "Score: 8\nReasoning: The generated text accurately reflects...",
    "details": {
      "Reasoning": "The generated text accurately reflects the source data",
      "Issues": "None"
    }
  }
}
```

### Evaluate Creativity

Evaluate the creativity and entertainment value of generated text.

**Endpoint**: `POST /api/eval/creativity`

**Request Body**:
```json
{
  "generated_text": "Wubba lubba dub dub! Rick exclaimed as he activated his portal gun."
}
```

**Example Request**:
```bash
curl -X POST http://localhost:5000/api/eval/creativity \
  -H "Content-Type: application/json" \
  -d '{"generated_text": "Wubba lubba dub dub!"}'
```

**Example Response**:
```json
{
  "success": true,
  "data": {
    "score": 7,
    "raw_response": "Score: 7\nReasoning: Good use of Rick's catchphrase...",
    "details": {
      "Reasoning": "Good use of Rick's catchphrase and action",
      "Strengths": "Captures Rick's personality well",
      "Improvements": "Could include more contextual details"
    }
  }
}
```

---

## Health Check

### Health Check

Check if the API is running and Gemini is available.

**Endpoint**: `GET /api/health`

**Example Request**:
```bash
curl http://localhost:5000/api/health
```

**Example Response**:
```json
{
  "success": true,
  "status": "healthy",
  "gemini_available": true
}
```

---

## Error Codes

| Status Code | Description |
|-------------|-------------|
| 200 | Success |
| 201 | Resource created successfully |
| 400 | Bad request (missing or invalid parameters) |
| 404 | Resource not found |
| 500 | Internal server error |
| 503 | Service unavailable (e.g., Gemini API not configured) |

---

## Rate Limiting

Currently, there are no rate limits implemented. For production use, consider:
- Implementing request rate limiting
- Caching frequently accessed data
- Using API keys for authentication

---

## Best Practices

1. **Always check `success` field** before processing `data`
2. **Handle errors gracefully** - show user-friendly messages
3. **Cache responses** when appropriate to reduce API calls
4. **Use batch operations** when fetching multiple resources
5. **Validate input** before sending requests

---

## Examples with Python

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Get all locations
response = requests.get(f"{BASE_URL}/locations")
locations = response.json()

# Search characters
response = requests.get(f"{BASE_URL}/characters/search", params={"name": "Rick"})
characters = response.json()

# Add a note
note_data = {
    "character_id": 1,
    "character_name": "Rick Sanchez",
    "note": "Genius inventor"
}
response = requests.post(f"{BASE_URL}/notes", json=note_data)
result = response.json()

# Semantic search
search_data = {
    "query": "genius scientists",
    "top_k": 5
}
response = requests.post(f"{BASE_URL}/search/semantic", json=search_data)
results = response.json()
```

---

## Examples with JavaScript

```javascript
const BASE_URL = "http://localhost:5000/api";

// Get all locations
fetch(`${BASE_URL}/locations?include_residents=true`)
  .then(response => response.json())
  .then(data => console.log(data));

// Search characters
fetch(`${BASE_URL}/characters/search?name=Rick`)
  .then(response => response.json())
  .then(data => console.log(data));

// Add a note
fetch(`${BASE_URL}/notes`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    character_id: 1,
    character_name: 'Rick Sanchez',
    note: 'Genius inventor'
  })
})
  .then(response => response.json())
  .then(data => console.log(data));

// Semantic search
fetch(`${BASE_URL}/search/semantic`, {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    query: 'genius scientists',
    top_k: 5
  })
})
  .then(response => response.json())
  .then(data => console.log(data));
```
