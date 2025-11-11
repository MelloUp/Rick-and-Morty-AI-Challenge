## Clean Architecture Refactoring

The project has been refactored to follow clean code principles and modular architecture patterns.

## New Project Structure

```
agency_fund_assignment/
├── src/                          # Main source package
│   ├── __init__.py
│   ├── config.py                 # Configuration management (dataclasses)
│   │
│   ├── models/                   # Data models (domain layer)
│   │   ├── __init__.py
│   │   ├── character.py          # Character dataclass
│   │   ├── location.py           # Location dataclass
│   │   └── note.py               # Note dataclass
│   │
│   ├── repositories/             # Data access layer (repository pattern)
│   │   ├── __init__.py
│   │   ├── base.py               # Base repository class
│   │   ├── note_repository.py    # Note CRUD operations
│   │   ├── cache_repository.py   # API response caching
│   │   └── embedding_repository.py # Embedding storage
│   │
│   ├── services/                 # Business logic layer
│   │   ├── __init__.py
│   │   ├── rick_morty_service.py # Rick & Morty API integration
│   │   ├── gemini_service.py     # Gemini AI operations
│   │   └── search_service.py     # Semantic search logic
│   │
│   ├── api/                      # Presentation layer
│   │   ├── __init__.py           # App factory
│   │   └── routes/               # Flask blueprints
│   │       ├── __init__.py       # Blueprint registration
│   │       ├── health.py         # Health check routes
│   │       ├── locations.py      # Location endpoints
│   │       ├── characters.py     # Character endpoints
│   │       ├── notes.py          # Note endpoints
│   │       ├── ai.py             # AI feature endpoints
│   │       └── search.py         # Search endpoints
│   │
│   ├── database/                 # Database layer
│   │   ├── __init__.py
│   │   ├── connection.py         # Connection management
│   │   └── migrations.py         # Schema migrations
│   │
│   └── utils/                    # Utilities
│       ├── __init__.py
│       └── exceptions.py         # Custom exceptions
│
├── tests/                        # Test package
│   ├── test_api.py
│   ├── test_services.py
│   └── test_repositories.py
│
├── app_new.py                    # Application entry point (clean)
├── app.py                        # Original app (for reference)
├── requirements.txt
└── README.md
```

## Architecture Principles

### 1. Separation of Concerns

Each layer has a single responsibility:

- **Models**: Data structures and domain logic
- **Repositories**: Data access and persistence
- **Services**: Business logic and orchestration
- **API**: HTTP request/response handling
- **Database**: Connection and schema management

### 2. Dependency Injection

Services receive their dependencies through constructors:

```python
class RickMortyService:
    def __init__(self, cache_repo: CacheRepository, config: APIConfig):
        self.cache_repo = cache_repo
        self.config = config
```

### 3. Repository Pattern

Data access is abstracted through repositories:

```python
class NoteRepository(BaseRepository):
    def create(self, character_id: int, character_name: str, note: str) -> int:
        # Database operations
        pass
```

### 4. Service Layer

Business logic is centralized in services:

```python
class SearchService:
    def search(self, query: str, top_k: int) -> List[SearchResult]:
        # Semantic search logic
        pass
```

### 5. Flask Blueprints

Routes are organized into logical blueprints:

```python
def create_notes_blueprint(note_repo: NoteRepository) -> Blueprint:
    bp = Blueprint('notes', __name__, url_prefix='/api/notes')
    # Route definitions
    return bp
```

## Key Improvements

### 1. Configuration Management

**Before**:
```python
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
```

**After**:
```python
@dataclass(frozen=True)
class GeminiConfig:
    api_key: Optional[str] = None
    model_name: str = "gemini-pro"

    @property
    def is_available(self) -> bool:
        return self.api_key is not None
```

### 2. Data Models

**Before**:
```python
character = {
    "id": 1,
    "name": "Rick",
    # ... dictionary manipulation
}
```

**After**:
```python
@dataclass(frozen=True)
class Character:
    id: int
    name: str
    status: str
    species: str

    def get_description(self) -> str:
        return f"{self.name} is a {self.species}"
```

### 3. Database Operations

**Before**:
```python
conn = sqlite3.connect("db.sqlite")
cursor = conn.cursor()
cursor.execute("INSERT ...")
conn.commit()
conn.close()
```

**After**:
```python
with db.get_connection() as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT ...")
    # Auto-commit and close
```

### 4. Error Handling

**Before**:
```python
try:
    data = fetch_data()
except Exception as e:
    return {"error": str(e)}, 500
```

**After**:
```python
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code

    def to_dict(self) -> Dict[str, Any]:
        return {"success": False, "error": self.message}
```

### 5. Dependency Management

**Before** (tight coupling):
```python
class Service:
    def __init__(self):
        self.db = Database()  # Creates dependency internally
```

**After** (dependency injection):
```python
class Service:
    def __init__(self, db: Database):
        self.db = db  # Receives dependency
```

## Pythonic Features Used

### 1. Dataclasses
```python
@dataclass(frozen=True)
class Note:
    id: int
    character_id: int
    note: str
```

### 2. Context Managers
```python
@contextmanager
def get_connection(self):
    conn = sqlite3.connect(self.db_path)
    try:
        yield conn
        conn.commit()
    except:
        conn.rollback()
        raise
    finally:
        conn.close()
```

### 3. Type Hints
```python
def search(self, query: str, top_k: int = 5) -> List[SearchResult]:
    pass
```

### 4. LRU Cache
```python
@lru_cache(maxsize=1)
def get_config() -> Config:
    return Config(...)
```

### 5. Property Decorators
```python
@property
def is_available(self) -> bool:
    return self.api_key is not None
```

### 6. List Comprehensions
```python
characters = [Character.from_dict(data) for data in results]
```

### 7. Factory Pattern
```python
def create_app(config=None) -> Flask:
    app = Flask(__name__)
    # Configure app
    return app
```

## Running the Clean Version

### Option 1: New Clean App
```bash
python app_new.py
```

### Option 2: Original App (for reference)
```bash
python app.py
```

Both versions provide the same functionality, but `app_new.py` uses the clean architecture.

## Benefits

### 1. Testability
- Easy to mock dependencies
- Isolated unit tests
- Clear test boundaries

### 2. Maintainability
- Single Responsibility Principle
- Easy to locate code
- Clear dependencies

### 3. Scalability
- Add new features without modifying existing code
- Swap implementations easily
- Horizontal scaling ready

### 4. Readability
- Self-documenting code
- Type hints provide clarity
- Logical organization

### 5. Reusability
- Services can be used independently
- Repositories are swappable
- Models are portable

## Design Patterns Used

1. **Repository Pattern**: Data access abstraction
2. **Service Layer Pattern**: Business logic encapsulation
3. **Factory Pattern**: App creation (`create_app`)
4. **Singleton Pattern**: Config management (`@lru_cache`)
5. **Dependency Injection**: Loose coupling
6. **Blueprint Pattern**: Route organization (Flask)

## SOLID Principles

### Single Responsibility
Each class has one reason to change:
- `NoteRepository`: Only changes if note storage logic changes
- `GeminiService`: Only changes if Gemini integration changes

### Open/Closed
Open for extension, closed for modification:
- Add new repositories without changing existing ones
- Add new services without modifying the service layer

### Liskov Substitution
Subtypes can replace base types:
- All repositories inherit from `BaseRepository`
- Can swap repository implementations

### Interface Segregation
Clients don't depend on unused interfaces:
- Each blueprint depends only on services it needs
- Repositories have focused interfaces

### Dependency Inversion
Depend on abstractions, not concretions:
- Services depend on repository interfaces
- Routes depend on service interfaces

## Migration Guide

To use the new structure:

1. **Import from new modules**:
   ```python
   from src.models import Character, Location
   from src.services import RickMortyService
   from src.repositories import NoteRepository
   ```

2. **Use dependency injection**:
   ```python
   config = get_config()
   db = get_db_connection()
   repo = NoteRepository(db)
   ```

3. **Handle custom exceptions**:
   ```python
   from src.utils import NotFoundError, ValidationError

   try:
       character = service.get_character(id)
   except NotFoundError:
       # Handle not found
   ```

## Testing Strategy

### Unit Tests
Test individual components in isolation:
```python
def test_note_repository_create(mock_db):
    repo = NoteRepository(mock_db)
    note_id = repo.create(1, "Rick", "Test note")
    assert note_id > 0
```

### Integration Tests
Test component interactions:
```python
def test_search_service_integration():
    service = SearchService(real_repo, real_gemini, real_rick_morty)
    results = service.search("scientist")
    assert len(results) > 0
```

### End-to-End Tests
Test full request/response cycle:
```python
def test_api_get_character(client):
    response = client.get('/api/characters/1')
    assert response.status_code == 200
```

## Future Enhancements

1. **Add interfaces (Protocols)**:
   ```python
   from typing import Protocol

   class Repository(Protocol):
       def get(self, id: int): ...
   ```

2. **Async support**:
   ```python
   async def get_character(self, id: int) -> Character:
       pass
   ```

3. **Event system**:
   ```python
   @event_listener('character_created')
   def on_character_created(character: Character):
       pass
   ```

4. **Caching decorator**:
   ```python
   @cached(ttl=60)
   def get_locations(self) -> List[Location]:
       pass
   ```

---

**The refactored code demonstrates production-ready Python best practices and clean architecture principles.**
