SERVICE_NAME=workspace
CONTAINER_NAME=palm-oil-workspace
IMAGE_NAME=palm-oil-dev

# Build the image
build:
	docker compose -f docker-compose.yml build

# Start containers
up:
	docker compose -f docker-compose.yml up -d

# Stop and remove containers
down:
	docker compose -f docker-compose.yml down -v

# Open shell in the dev container
bash:
	docker exec -it $(CONTAINER_NAME) bash

# Start Airflow services
airflow-up:
	docker compose -f docker-compose-airflow.yml up -d

# Stop Airflow services
airflow-down:
	docker compose -f docker-compose-airflow.yml down -v

# Start everything (workspace + Airflow)
full-up:
	docker compose -f docker-compose.yml -f docker-compose-airflow.yml up -d

# Stop everything
full-down:
	docker compose -f docker-compose.yml -f docker-compose-airflow.yml down -v

# View Airflow logs
airflow-logs:
	docker compose -f docker-compose-airflow.yml logs -f

# Access Airflow bash (useful for CLI commands)
airflow-bash:
	docker compose -f docker-compose-airflow.yml exec airflow-scheduler bash

# Rebuild from scratch
rebuild:
	docker compose -f docker-compose.yml -f docker-compose-airflow.yml down -v --remove-orphans
	docker compose -f docker-compose.yml build --no-cache
	docker compose -f docker-compose.yml -f docker-compose-airflow.yml up -d

# Logs for workspace
logs:
	docker compose -f docker-compose.yml logs -f $(SERVICE_NAME)

# Comprehensive cleanup - removes everything
clean:
	@echo "🧹 Starting comprehensive cleanup..."
	-docker compose -f docker-compose.yml -f docker-compose-airflow.yml down -v --remove-orphans 2>/dev/null || true
	-docker rm -f palm-oil-workspace 2>/dev/null || true
	@if [ -n "$$(docker images -f "dangling=true" -q)" ]; then \
		docker rmi $$(docker images -f "dangling=true" -q) 2>/dev/null || true; \
	fi
	-docker rmi -f palm-oil-dev 2>/dev/null || true
	-docker volume prune -f 2>/dev/null || true
	-docker network prune -f 2>/dev/null || true
	-docker builder prune -f 2>/dev/null || true
	-sudo rm -rf ./volumes 2>/dev/null || true
	@echo "✅ Cleanup complete!"

# Show current status
status:
	@echo "📊 Docker Status:"
	@echo "================"
	@echo "🐳 Running Containers:"
	@docker ps --format "table {{.Names}}\t{{.Image}}\t{{.Status}}\t{{.Ports}}"
	@echo ""
	@echo "🖼️ Images:"
	@docker images --format "table {{.Repository}}\t{{.Tag}}\t{{.ID}}\t{{.Size}}" | grep -E "(palm-oil|postgres|airflow)" || echo "No project images found"
	@echo ""
	@echo "📦 Volumes:"
	@docker volume ls --format "table {{.Name}}\t{{.Driver}}" | grep -E "(palm-oil|airflow)" || echo "No project volumes found"

# Initialize Airflow (run once)
airflow-init:
	docker compose -f docker-compose-airflow.yml up airflow-init

# Help
help:
	@echo "CryptoAnalytics Pipeline - Available Commands:"
	@echo "========================================="
	@echo "build         - Build the development image"
	@echo "up            - Start workspace containers in background"
	@echo "down          - Stop and remove workspace containers"
	@echo "bash          - Open shell in workspace container"
	@echo "airflow-up    - Start Airflow services"
	@echo "airflow-down  - Stop Airflow services"
	@echo "airflow-init  - Initialize Airflow (run once after setup)"
	@echo "airflow-bash  - Open shell in Airflow scheduler"
	@echo "full-up       - Start everything (workspace + Airflow)"
	@echo "full-down     - Stop everything"
	@echo "airflow-logs  - View Airflow logs"
	@echo "logs          - Show workspace container logs"
	@echo "rebuild       - Clean rebuild from scratch"
	@echo "clean         - 🧹 REMOVE EVERYTHING (images, volumes, cache, logs)"
	@echo "status        - Show current Docker status"
	@echo "help          - Show this help message"