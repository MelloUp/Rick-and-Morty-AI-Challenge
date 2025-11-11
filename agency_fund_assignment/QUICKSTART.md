# Quick Start Guide

## 🚀 Get Running in 3 Minutes

### Step 1: Install Dependencies

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure API Key

```bash
# Copy environment template
cp .env.example .env

# Edit .env and add your Gemini API key
# Get key from: https://makersuite.google.com/app/apikey
```

Edit `.env`:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 3: Run the Application

```bash
# Option 1: Use quick start script
./run.sh          # Unix/Mac/Linux
run.bat           # Windows

# Option 2: Run directly
python app.py
```

### Step 4: Open Browser

Navigate to: **http://localhost:5000**

---

## ✅ Verify Installation

After running the app, you should see:

```
============================================================
Rick & Morty AI Challenge - Clean Architecture
============================================================

Server starting at http://127.0.0.1:5000
Gemini AI: Enabled

Press Ctrl+C to stop
```

---

## 🧪 Run Tests

```bash
# Run all tests
pytest -v

# Run specific tests
pytest tests/test_api.py -v
pytest tests/test_llm_evals.py -v -s
```

---

## 📁 Project Structure

```
agency_fund_assignment/
├── src/                    # Clean architecture modules
│   ├── models/            # Dataclass models
│   ├── repositories/      # Database access
│   ├── services/          # Business logic
│   ├── api/routes/        # Flask blueprints
│   ├── database/          # DB management
│   └── utils/             # Utilities
├── tests/                 # Test suite
├── app.py                 # Entry point
├── index.html            # Frontend
└── requirements.txt      # Dependencies
```

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError"
**Solution**: Make sure dependencies are installed
```bash
pip install -r requirements.txt
```

### Issue: "Gemini API not configured"
**Solution**: Add GEMINI_API_KEY to .env file
```bash
echo "GEMINI_API_KEY=your_key" > .env
```

### Issue: "Address already in use"
**Solution**: Change port in .env
```bash
echo "FLASK_PORT=5001" >> .env
```

### Issue: "Database is locked"
**Solution**: Close other connections or delete .db file
```bash
rm -f *.db
```

---

## 📚 Next Steps

1. **Explore the UI**: Open http://localhost:5000
2. **Try AI Features**: Generate location summaries
3. **Semantic Search**: Index characters and search
4. **Read Docs**: Check API_DOCUMENTATION.md

---

## 🎯 Key Features to Try

### 1. Location Explorer
- Click "Locations" tab → "Load All Locations"
- Click any location to see residents

### 2. Character Search
- Click "Characters" tab
- Search for "Rick" or "Morty"
- Click a character to add notes

### 3. AI Generation
- Click "AI Features" tab
- Try Location Summary (ID: 1)
- Try Character Dialogue (IDs: 1, 2)

### 4. Semantic Search
- Click "Semantic Search" tab
- Click "Index Characters" (takes ~1 min)
- Search: "genius scientists from Earth"

---

## 🏗️ Architecture Highlights

This project uses **clean architecture** with:

✅ **Dataclasses** for type-safe models
✅ **Repository Pattern** for data access
✅ **Service Layer** for business logic
✅ **Dependency Injection** for loose coupling
✅ **Flask Blueprints** for organized routes
✅ **Custom Exceptions** for error handling

---

## 📊 API Endpoints

- `GET /api/health` - Health check
- `GET /api/locations` - Get all locations
- `GET /api/characters/<id>` - Get character
- `POST /api/notes` - Add note
- `GET /api/ai/location-summary/<id>` - AI summary
- `POST /api/search/semantic` - Semantic search

Full API docs: **API_DOCUMENTATION.md**

---

**Ready to explore!** 🎉
