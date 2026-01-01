# 🌐 Global Trend Intelligence System (GTIS)

AI-driven analytics platform that monitors, predicts, and explains global search trends in real-time.

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- 4GB+ RAM__



### Installation (3 steps)

1. **Extract the project**
```bash
unzip gtis-project.zip
cd gtis-project
```

2. **Run setup**
```bash
chmod +x setup.sh
./setup.sh
```

3. **Access applications**
- Frontend Dashboard: http://localhost:8501
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

## ✨ Features

- 🔮 **Trend Forecasting**: Prophet, ARIMA, LSTM models
- 🎯 **Emerging Topics**: Detect trends before they peak
- 🧠 **NLP Analysis**: Semantic clustering with S-BERT
- 🗺️ **Geographic Insights**: Regional interest distribution
- 🔗 **Correlation Analysis**: Link trends to real-world data
- 📊 **Interactive Dashboard**: Beautiful Streamlit UI

## 📖 Usage

### Analyze Trends
```python
curl -X POST "http://localhost:8000/api/fetch-trends" \
  -H "Content-Type: application/json" \
  -d '{"keywords": ["AI", "ML"], "timeframe": "today 12-m"}'
```

### Generate Predictions
```python
curl -X POST "http://localhost:8000/api/predict-trends" \
  -H "Content-Type: application/json" \
  -d '{"keyword": "artificial intelligence", "periods": 30}'
```

## 🛠️ Development

```bash
# View logs
docker-compose logs -f

# Run tests
docker-compose exec backend pytest -v

# Restart services
docker-compose restart

# Stop services
docker-compose down
```

## 📂 Project Structure

```
gtis-project/
├── backend/           # FastAPI backend
├── frontend/          # Streamlit dashboard
├── tests/            # Test suite
├── data/             # Database storage
├── models/           # ML model cache
└── docker-compose.yml
```

## 🧪 Testing

```bash
make test
# or
docker-compose exec backend pytest -v
```

## 📊 Tech Stack

- **Backend**: FastAPI, Python 3.11
- **Frontend**: Streamlit, Plotly
- **ML**: Prophet, ARIMA, LSTM, S-BERT
- **Data**: PyTrends, SQLite
- **Deploy**: Docker, Docker Compose

## 🤝 Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📝 License

MIT License - see LICENSE file

## 🙏 Acknowledgments

- Google Trends API
- Prophet by Facebook
- Sentence-BERT by UKPLab
- FastAPI & Streamlit teams

---

Built with ❤️ for data science

