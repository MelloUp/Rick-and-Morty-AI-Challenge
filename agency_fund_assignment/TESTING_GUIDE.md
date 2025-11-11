# Testing Guide

Quick reference for testing all features of the Rick & Morty AI Challenge application.

## Prerequisites

1. **Start the application**:
   ```bash
   # Unix/Mac
   ./run.sh

   # Windows
   run.bat

   # Or manually
   python app.py
   ```

2. **Ensure Gemini API key is set** in `.env` file for AI features

---

## Manual Testing Checklist

### 1. Frontend UI Testing

#### Locations Tab
- [ ] Click "Locations" tab
- [ ] Click "Load All Locations" button
- [ ] Verify locations are displayed in grid
- [ ] Click on a location card
- [ ] Verify modal shows location details and residents
- [ ] Click on a resident to view their details
- [ ] Close modal

#### Characters Tab
- [ ] Click "Characters" tab
- [ ] Enter "Rick" in search box
- [ ] Click "Search" or press Enter
- [ ] Verify search results appear
- [ ] Click on a character card
- [ ] Verify character details modal opens
- [ ] Scroll to notes section
- [ ] Add a note in the textarea
- [ ] Click "Save Note"
- [ ] Verify note appears in the list
- [ ] Refresh page and verify note persists

#### AI Features Tab
- [ ] Click "AI Features" tab

**Location Summary**
- [ ] Enter location ID: `1`
- [ ] Click "Generate Summary"
- [ ] Verify Rick & Morty style summary appears
- [ ] Try with different location IDs (2, 3, 20)

**Character Dialogue**
- [ ] Enter Character 1 ID: `1` (Rick)
- [ ] Enter Character 2 ID: `2` (Morty)
- [ ] Click "Generate Dialogue"
- [ ] Verify dialogue appears
- [ ] Try with different character pairs

**Character Analysis**
- [ ] Enter Character ID: `1`
- [ ] Click "Analyze Character"
- [ ] Verify analysis appears
- [ ] Try with different character IDs

#### Semantic Search Tab
- [ ] Click "Semantic Search" tab
- [ ] Click "Index Characters" (first time only)
- [ ] Wait for indexing to complete (~1 minute)
- [ ] Enter query: `genius scientists`
- [ ] Set results to: `5`
- [ ] Click "Search"
- [ ] Verify results are ranked by similarity
- [ ] Try different queries:
  - `young student`
  - `characters from Earth`
  - `alien species`
  - `human characters`

---

## API Testing with cURL

### Health Check
```bash
curl http://localhost:5000/api/health
```

### Locations
```bash
# Get all locations
curl http://localhost:5000/api/locations

# Get locations with residents
curl "http://localhost:5000/api/locations?include_residents=true"

# Get specific location
curl http://localhost:5000/api/locations/1
```

### Characters
```bash
# Get character details
curl http://localhost:5000/api/characters/1

# Search characters
curl "http://localhost:5000/api/characters/search?name=Rick"
```

### Notes
```bash
# Add a note
curl -X POST http://localhost:5000/api/notes \
  -H "Content-Type: application/json" \
  -d '{
    "character_id": 1,
    "character_name": "Rick Sanchez",
    "note": "Test note from cURL"
  }'

# Get notes for character
curl http://localhost:5000/api/notes/1

# Update note (replace <note_id> with actual ID)
curl -X PUT http://localhost:5000/api/notes/<note_id> \
  -H "Content-Type: application/json" \
  -d '{"note": "Updated note content"}'

# Delete note
curl -X DELETE http://localhost:5000/api/notes/<note_id>
```

### AI Features
```bash
# Generate location summary
curl http://localhost:5000/api/ai/location-summary/1

# Generate character dialogue
curl -X POST http://localhost:5000/api/ai/character-dialogue \
  -H "Content-Type: application/json" \
  -d '{
    "character1_id": 1,
    "character2_id": 2
  }'

# Generate character analysis
curl http://localhost:5000/api/ai/character-analysis/1
```

### Semantic Search
```bash
# Index characters
curl -X POST http://localhost:5000/api/search/index-characters \
  -H "Content-Type: application/json" \
  -d '{}'

# Perform semantic search
curl -X POST http://localhost:5000/api/search/semantic \
  -H "Content-Type: application/json" \
  -d '{
    "query": "genius scientists from Earth",
    "top_k": 5
  }'
```

### Evaluation
```bash
# Evaluate factual consistency
curl -X POST http://localhost:5000/api/eval/factual-consistency \
  -H "Content-Type: application/json" \
  -d '{
    "generated_text": "Rick is a scientist who travels dimensions",
    "source_data": {
      "name": "Rick Sanchez",
      "species": "Human",
      "occupation": "Scientist"
    }
  }'

# Evaluate creativity
curl -X POST http://localhost:5000/api/eval/creativity \
  -H "Content-Type: application/json" \
  -d '{
    "generated_text": "Wubba lubba dub dub! Rick exclaimed as he activated his portal gun."
  }'
```

---

## Automated Testing

### Run All Tests
```bash
pytest -v
```

### Run API Tests Only
```bash
pytest test_api.py -v
```

### Run LLM Evaluation Tests Only
```bash
# Requires GEMINI_API_KEY in .env
pytest test_llm_evals.py -v -s
```

### Run Specific Test Class
```bash
pytest test_api.py::TestLocationEndpoints -v
pytest test_llm_evals.py::TestLocationSummaryEvaluation -v
```

### Run with Coverage
```bash
pip install pytest-cov
pytest --cov=. --cov-report=html
open htmlcov/index.html
```

---

## Test Coverage Checklist

### API Endpoints (test_api.py)
- [x] Health check
- [x] Get all locations
- [x] Get locations with residents
- [x] Get specific location
- [x] Get invalid location (404)
- [x] Get character by ID
- [x] Search characters by name
- [x] Search with no results
- [x] Add note (CRUD - Create)
- [x] Get notes (CRUD - Read)
- [x] Update note (CRUD - Update)
- [x] Delete note (CRUD - Delete)
- [x] AI endpoints structure validation
- [x] Edge cases (negative IDs, special chars, etc.)

### LLM Evaluations (test_llm_evals.py)
- [x] Location summary generation
- [x] Location summary factual consistency
- [x] Location summary creativity
- [x] Character dialogue generation
- [x] Character dialogue creativity
- [x] Character analysis generation
- [x] Character analysis factual consistency
- [x] Embedding generation
- [x] Embedding similarity
- [x] Semantic search relevance
- [x] Evaluation metrics validation
- [x] Edge cases (empty text, long text, contradictions)

---

## Performance Testing

### Load Testing with Apache Bench
```bash
# Install apache2-utils (Ubuntu) or httpd (Mac)
# Test locations endpoint
ab -n 100 -c 10 http://localhost:5000/api/locations

# Test character search
ab -n 100 -c 10 "http://localhost:5000/api/characters/search?name=Rick"
```

### Response Time Benchmarks

**Expected Response Times** (without caching):
- Health check: < 10ms
- Get locations (cached): < 50ms
- Get locations (first time): < 3s
- Character search: < 500ms
- AI generation: 2-5s (depends on Gemini API)
- Semantic search: 100-500ms (after indexing)

---

## Edge Cases to Test

### Invalid Inputs
- [ ] Negative character IDs
- [ ] Character ID = 0
- [ ] Very large character ID (999999)
- [ ] Special characters in search (`@#$%`)
- [ ] Empty search query
- [ ] Empty note content
- [ ] Very long note (10,000 characters)
- [ ] Unicode characters in notes
- [ ] Malformed JSON in POST requests

### Error Scenarios
- [ ] Gemini API key not set
- [ ] Invalid location ID
- [ ] Non-existent character
- [ ] Update non-existent note
- [ ] Delete non-existent note
- [ ] Semantic search before indexing

### Success Scenarios
- [ ] All API endpoints return 200/201 for valid inputs
- [ ] Notes persist across server restarts
- [ ] Cache works correctly
- [ ] Embeddings are generated consistently
- [ ] Semantic search returns relevant results

---

## Browser Compatibility Testing

Test the UI in:
- [ ] Chrome/Chromium
- [ ] Firefox
- [ ] Safari
- [ ] Edge

Test responsive design:
- [ ] Desktop (1920x1080)
- [ ] Tablet (768x1024)
- [ ] Mobile (375x667)

---

## Accessibility Testing

- [ ] Keyboard navigation works
- [ ] Focus states are visible
- [ ] Color contrast is sufficient
- [ ] Images have alt text
- [ ] Buttons have descriptive text
- [ ] Forms have labels

---

## Security Testing

- [ ] API key not exposed in frontend
- [ ] Input validation prevents SQL injection
- [ ] XSS protection in user inputs
- [ ] CORS headers configured correctly
- [ ] Error messages don't leak sensitive info

---

## Common Issues & Solutions

### Issue: "Gemini API not configured"
**Solution**: Add `GEMINI_API_KEY` to `.env` file

### Issue: "No character embeddings found"
**Solution**: Click "Index Characters" in Semantic Search tab

### Issue: Tests fail with "Connection refused"
**Solution**: Make sure Flask app is running on port 5000

### Issue: "Module not found" error
**Solution**: Install dependencies with `pip install -r requirements.txt`

### Issue: Database locked error
**Solution**: Close all other connections to the database

---

## Regression Testing Checklist

After making changes, test:
- [ ] All API endpoints still work
- [ ] UI loads correctly
- [ ] Notes persist correctly
- [ ] AI features generate content
- [ ] Semantic search returns results
- [ ] All tests pass
- [ ] No console errors in browser

---

## Test Data

### Sample Location IDs
- 1: Earth (C-137)
- 2: Abadango
- 3: Citadel of Ricks
- 20: Worldender's lair

### Sample Character IDs
- 1: Rick Sanchez
- 2: Morty Smith
- 3: Summer Smith
- 4: Beth Smith
- 5: Jerry Smith

### Sample Search Queries (Semantic)
- "genius scientists"
- "young student from Earth"
- "alien species"
- "characters who are dead"
- "human characters from dimension C-137"

---

## Evaluation Metrics

### LLM Output Quality Thresholds

**Factual Consistency**:
- Acceptable: ≥ 5/10
- Good: ≥ 7/10
- Excellent: ≥ 9/10

**Creativity**:
- Acceptable: ≥ 4/10
- Good: ≥ 6/10
- Excellent: ≥ 8/10

**Semantic Similarity**:
- Relevant: ≥ 0.5
- Highly Relevant: ≥ 0.7
- Exact Match: ≥ 0.9

---

## Continuous Integration

For CI/CD pipeline:

```yaml
# Example .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: pytest test_api.py -v
```

---

**Happy Testing!** 🚀
