# Quantum Hackathon - Swift API with MySQL

This project provides a Swift-based REST API with MySQL database integration for the Qiskit Hackathon at World of QUANTUM. The API allows you to store user information, quantum experiments, and their results.

## Features

- **User Management**: Register hackathon participants with their team information
- **Quantum Experiment Tracking**: Store quantum circuit configurations and results
- **Statistics**: Get insights about experiments and success rates
- **MySQL Integration**: Persistent data storage with relationships
- **REST API**: Easy integration with web frontends or mobile apps

## Prerequisites

- Swift 5.7 or later
- Docker and Docker Compose (for MySQL setup)
- MySQL 8.0 (if not using Docker)

## Quick Start

### 1. Set Up MySQL Database

Using Docker (Recommended):
```bash
# Start MySQL and phpMyAdmin
docker-compose up -d

# Check if containers are running
docker ps
```

The database will be available at:
- MySQL: `localhost:3306`
- phpMyAdmin: `http://localhost:8080`

### 2. Configure Environment

Copy the example environment file:
```bash
cp .env.example .env
```

Modify `.env` if needed with your database credentials.

### 3. Install Dependencies and Run

```bash
# Resolve Swift package dependencies
swift package resolve

# Build the project
swift build

# Run the server
swift run QuantumServer
```

The API will be available at `http://localhost:8080`

## API Endpoints

### Users

- `GET /api/users` - Get all users
- `POST /api/users` - Create a new user
- `GET /api/users/:id` - Get user by ID
- `GET /api/users/:id/experiments` - Get user's experiments

### Quantum Experiments

- `GET /api/experiments` - Get all experiments
- `POST /api/experiments` - Create a new experiment
- `GET /api/experiments/:id` - Get experiment by ID
- `PUT /api/experiments/:id/results` - Update experiment results

### Statistics

- `GET /api/stats` - Get hackathon statistics

## Example Usage

### Creating a User

```bash
curl -X POST http://localhost:8080/api/users \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_quantum",
    "email": "alice@example.com",
    "fullName": "Alice Johnson",
    "teamName": "Quantum Pioneers",
    "experienceLevel": "Advanced"
  }'
```

### Creating a Quantum Experiment

```bash
curl -X POST http://localhost:8080/api/experiments \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Bell State Experiment",
    "circuitType": "Entanglement",
    "qubitCount": 2,
    "gateSequence": "H(0), CNOT(0,1)",
    "user": {"id": "USER_UUID_HERE"}
  }'
```

### Updating Experiment Results

```bash
curl -X PUT http://localhost:8080/api/experiments/EXPERIMENT_ID/results \
  -H "Content-Type: application/json" \
  -d '{
    "measurementResults": "00: 0.48, 11: 0.52",
    "successProbability": 0.95
  }'
```

## Database Schema

### Users Table
- `id` (UUID, Primary Key)
- `username` (String, Unique)
- `email` (String, Unique)
- `full_name` (String)
- `team_name` (String, Optional)
- `experience_level` (String)
- `created_at` (DateTime)
- `updated_at` (DateTime)

### Quantum Experiments Table
- `id` (UUID, Primary Key)
- `name` (String)
- `circuit_type` (String)
- `qubit_count` (Integer)
- `gate_sequence` (String)
- `measurement_results` (String, Optional)
- `success_probability` (Double, Optional)
- `user_id` (UUID, Foreign Key to Users)
- `created_at` (DateTime)
- `updated_at` (DateTime)

## Development

### Running Tests

```bash
swift test
```

### Database Management

Access phpMyAdmin at `http://localhost:8080` to manage your MySQL database visually.

### Resetting Database

To reset the database and start fresh:

```bash
# Stop containers
docker-compose down

# Remove volumes (this will delete all data!)
docker volume rm quantum-hackathon_mysql_data

# Start again
docker-compose up -d
```

## Integration with Jupyter Notebooks

You can integrate this API with the existing Qiskit Jupyter notebooks by making HTTP requests to store experiment results:

```python
import requests
import json

# Store experiment result
def store_experiment_result(user_id, name, circuit_type, qubits, gates, results):
    experiment_data = {
        "name": name,
        "circuitType": circuit_type,
        "qubitCount": qubits,
        "gateSequence": gates,
        "measurementResults": results,
        "user": {"id": user_id}
    }
    
    response = requests.post(
        "http://localhost:8080/api/experiments",
        headers={"Content-Type": "application/json"},
        data=json.dumps(experiment_data)
    )
    
    return response.json()
```

## Troubleshooting

### MySQL Connection Issues

1. Check if MySQL container is running: `docker ps`
2. Verify environment variables in `.env`
3. Check MySQL logs: `docker logs quantum_hackathon_mysql`

### Swift Build Issues

1. Clean and rebuild: `swift package clean && swift build`
2. Update dependencies: `swift package update`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is part of the Qiskit Hackathon at World of QUANTUM event.