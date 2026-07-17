
# ⚽ Football Game Statistics Simulator

A comprehensive football match simulator that generates realistic player and team statistics using Python. Features multiple deployment options including standalone CLI, web application, REST API, and cloud deployment.

## Features

- **Match Simulation**: Simulate realistic football matches with configurable game events
- **Player Statistics**: Track individual player performance (goals, assists, passes, tackles, etc.)
- **Team Statistics**: Aggregate team-level metrics including possession percentage
- **Interactive Dashboard**: Web-based UI for running simulations and viewing results
- **REST API**: API endpoints for programmatic access
- **Multiple Deployment Options**: Standalone script, web app, Docker, cloud platforms
- **CI/CD Pipeline**: Automated testing and deployment with GitHub Actions

## Quick Start

### 1. Standalone Script

```bash
# Install dependencies
pip install -r requirements.txt

# Run simulation
python football_simulator.py
```

### 2. Web Application (Local)

```bash
# Install dependencies
pip install -r requirements.txt

# Run Flask app
python app.py

# Open browser to http://localhost:5000
```

### 3. Docker

```bash
# Build image
docker build -t football-simulator .

# Run container
docker run -p 5000:5000 football-simulator

# Open browser to http://localhost:5000
```

### 4. Docker Compose

```bash
# Start services
docker-compose up

# Open browser to http://localhost
```

## Project Structure

```
.
├── football_simulator.py       # Core simulator logic
├── app.py                       # Flask web application
├── requirements.txt             # Python dependencies
├── Dockerfile                   # Docker configuration
├── docker-compose.yml          # Multi-container setup
├── nginx.conf                  # Nginx reverse proxy
├── .github/workflows/          # CI/CD workflows
├── templates/                  # HTML templates
│   └── index.html             # Web dashboard
├── static/                     # Static files
│   ├── style.css              # CSS styles
│   └── script.js              # JavaScript
└── tests/                      # Unit tests
    └── test_simulator.py      # Test cases
```

## API Endpoints

### Run Simulation
```
GET /api/simulate?events=100
```

Response:
```json
{
  "success": true,
  "match_result": {
    "team_a_name": "FC Alpha",
    "team_a_score": 15,
    "team_b_name": "Sporting Beta",
    "team_b_score": 20
  },
  "team_a_stats": {...},
  "team_b_stats": {...},
  "team_a_players": [...],
  "team_b_players": [...]
}
```

### Health Check
```
GET /api/health
```

Response:
```json
{
  "status": "healthy",
  "message": "Football Simulator API is running"
}
```

## Class Documentation

### Player
Represents a football player with attributes and performance statistics.

**Attributes:**
- `name`: Player name
- `offense`: Offensive skill (0-100)
- `defense`: Defensive skill (0-100)
- `stamina`: Player stamina (0-100)
- `stats`: Dictionary of match statistics

### Team
Represents a football team with multiple players.

**Methods:**
- `get_offensive_players()`: Returns players sorted by offensive ability
- `get_defensive_players()`: Returns players sorted by defensive ability

## Configuration

### Game Events
Modify `TOTAL_GAME_EVENTS` in `football_simulator.py` to change match duration (default: 100 events).

### Event Weights
Adjust event type probabilities in `simulate_game_event()`:
- Pass: 40%
- Shot: 30%
- Tackle: 15%
- Foul: 10%
- Interception: 5%

## Cloud Deployment

### AWS EC2
```bash
# SSH into instance
ssh -i key.pem ec2-user@instance-ip

# Clone repository and setup
git clone https://github.com/wop27812-creator/Python-.git
cd Python-
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
gunicorn -b 0.0.0.0:5000 app:app
```

### Heroku
```bash
# Create Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
git push heroku main
```

### Google Cloud Run
```bash
# Deploy
gcloud run deploy football-simulator \
  --source . \
  --platform managed \
  --region us-central1
```

### Azure App Service
```bash
# Deploy using Azure CLI
az webapp up --name football-simulator --runtime python:3.11
```

## Testing

```bash
# Run tests
python -m pytest tests/

# Run with coverage
python -m pytest tests/ --cov=football_simulator
```

## Performance Statistics

Example simulation output (100 events):
- **Match Duration**: < 1 second
- **Memory Usage**: < 50 MB
- **Typical Goals**: 15-25 per team
- **Shot Accuracy**: ~75% on target

## Future Enhancements

- [ ] Advanced player injury simulation
- [ ] Season-long tournament mode
- [ ] Player transfer system
- [ ] Historical match data import
- [ ] Advanced statistics visualization
- [ ] Real-time match commentary
- [ ] Mobile app integration
- [ ] Database persistence

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Author

Created by wisdom peter (wop27812-creator)

## Support

For issues, questions, or suggestions, please open a GitHub issue.

---

**Built with ❤️ for football enthusiasts and data analysts**
