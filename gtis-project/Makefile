.PHONY: help build up down restart logs test clean

help:
	@echo "GTIS - Global Trend Intelligence System"
	@echo ""
	@echo "Available commands:"
	@echo "  make build     - Build Docker containers"
	@echo "  make up        - Start all services"
	@echo "  make down      - Stop all services"
	@echo "  make restart   - Restart all services"
	@echo "  make logs      - View logs"
	@echo "  make test      - Run tests"
	@echo "  make clean     - Clean up"

build:
	docker-compose build

up:
	docker-compose up -d
	@echo "✅ Services started!"
	@echo "   Frontend: http://localhost:8501"
	@echo "   Backend: http://localhost:8000"

down:
	docker-compose down

restart:
	docker-compose restart

logs:
	docker-compose logs -f

test:
	docker-compose exec backend pytest -v

clean:
	docker-compose down -v
	rm -rf data/*.db models/cache/*
