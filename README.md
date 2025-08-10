# Sensor Data Collection Backend

A FastAPI-based backend system for collecting acceleration and gyroscope data from IoT sensors via Bluetooth, using Kafka for real-time data streaming and MySQL for persistent storage.

## Project Directory Structure

```
sensor_reading_backend/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py              # Configuration settings
│   ├── database.py            # Database connection and setup
│   ├── models/
│   │   ├── __init__.py
│   │   ├── sensor.py          # Sensor database models
│   │   └── sensor_data.py     # Sensor data database models
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── sensor.py          # Sensor Pydantic schemas
│   │   └── sensor_data.py     # Sensor data Pydantic schemas
│   ├── api/
│   │   ├── __init__.py
│   │   ├── deps.py            # API dependencies
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── api.py         # API router
│   │       ├── endpoints/
│   │       │   ├── __init__.py
│   │       │   ├── sensors.py # Sensor management endpoints
│   │       │   ├── data.py    # Data collection endpoints
│   │       │   └── health.py  # Health check endpoints
│   ├── services/
│   │   ├── __init__.py
│   │   ├── bluetooth.py       # Bluetooth communication service
│   │   ├── kafka_producer.py  # Kafka producer service
│   │   ├── kafka_consumer.py  # Kafka consumer service
│   │   └── data_processor.py  # Data processing service
│   ├── core/
│   │   ├── __init__.py
│   │   ├── logging.py         # Logging configuration
│   │   └── exceptions.py      # Custom exceptions
│   └── utils/
│       ├── __init__.py
│       └── helpers.py         # Utility functions
├── migrations/
│   ├── versions/              # Alembic migration files
│   ├── alembic.ini           # Alembic configuration
│   └── env.py                # Alembic environment
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # Test configuration
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_sensors.py   # Sensor API tests
│   │   └── test_data.py      # Data API tests
│   ├── test_services/
│   │   ├── __init__.py
│   │   ├── test_bluetooth.py # Bluetooth service tests
│   │   └── test_kafka.py     # Kafka service tests
│   └── test_models/
│       ├── __init__.py
│       └── test_sensor.py    # Model tests
├── scripts/
│   ├── init_db.py            # Database initialization
│   ├── start_consumer.py     # Start Kafka consumer
│   └── seed_data.py          # Sample data seeding
├── docker/
│   ├── Dockerfile            # Application Dockerfile
│   ├── docker-compose.yml    # Development environment
│   └── docker-compose.prod.yml # Production environment
├── docs/
│   ├── api.md               # API documentation
│   ├── deployment.md        # Deployment guide
│   └── development.md       # Development setup
├── .env.example             # Environment variables template
├── .gitignore              # Git ignore file
├── requirements.txt        # Python dependencies
├── pyproject.toml         # Project configuration
├── README.md              # This file
└── architecture_design.md # System architecture documentation
```

## Quick Start

### 1. Environment Setup
```bash
# Clone the repository
git clone <repository-url>
cd sensor_reading_backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env with your configuration
# - Database connection string
# - Kafka bootstrap servers
# - Bluetooth settings
```

### 3. Database Setup
```bash
# Initialize database
python scripts/init_db.py

# Run migrations
alembic upgrade head
```

### 4. Start Services
```bash
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Start Kafka consumer (in separate terminal)
python scripts/start_consumer.py
```

### 5. Development with Docker
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

## Key Components

- **FastAPI Server**: REST API with automatic documentation
- **Bluetooth Service**: IoT sensor communication
- **Kafka Integration**: Real-time data streaming
- **MySQL Database**: Persistent data storage
- **Data Models**: Pydantic validation schemas

## API Documentation

Once the server is running, visit:
- **Interactive API Docs**: http://localhost:8000/docs
- **ReDoc Documentation**: http://localhost:8000/redoc

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app

# Run specific test file
pytest tests/test_api/test_sensors.py
```

## Monitoring

- **Health Check**: `GET /health`
- **System Metrics**: `GET /metrics`
- **Service Status**: `GET /status`

## Contributing

1. Follow the project structure outlined above
2. Add tests for new functionality
3. Update documentation as needed
4. Follow Python PEP 8 style guidelines

## License

[Add your license information here]