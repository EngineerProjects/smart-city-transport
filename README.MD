# Smart City IoT Data Platform

**Goal:** Build an end-to-end data engineering and machine learning platform that analyzes urban transportation patterns, predicts demand, and provides real-time insights for smart city optimization using NYC taxi data, weather APIs, and IoT sensor data.

## Why Transport Data?

Transportation is the backbone of urban life and generates massive, rich datasets perfect for learning modern data engineering. This project provides:
- Multi-modal data streams (historical files + real-time APIs)
- Real business impact (route optimization, demand forecasting, policy analysis)
- Rich ML opportunities (time series, geospatial, computer vision)
- Current relevance (congestion pricing effects, post-pandemic patterns)
- Scalable architecture that mirrors real-world enterprise data platforms

## Primary Use Case

**Weather-Driven Demand Forecasting**: Predict hourly taxi demand by NYC zone using weather and air quality conditions to optimize driver allocation and reduce passenger wait times during weather events.

See :

- [docs/0_PROJECT_PLAN.md](docs/0_PROJECT_PLAN.md) for detailed execution roadmap and task breakdown.
- [docs/1_probematic.md](docs/1_probematic.md) for the problem definition
- [datas/Instruction.md](datas/Instruction.md) to download all needed datas to start.

## Data Sources

### Primary Dataset
- **NYC Taxi & Limousine Commission (TLC) Trip Records**
  - **Source**: https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
  - **Format**: Parquet files (monthly)
  - **Coverage**: 2009-2025 (using 2023-2025 for this project)
  - **Volume**: ~3.4M records/month, 100M+ total records
  - **Data Types**: Yellow Taxi, Green Taxi, For-Hire Vehicle (FHV), High Volume FHV

### Real-Time APIs
- **Weather Data**: Open-Meteo API (completely free, no API key required)
  - **API Documentation**: https://open-meteo.com/en/docs
  - **Features**: Hourly weather forecasts, historical data, global coverage
- **Air Quality Data**: Open-Meteo Air Quality API (free)
  - **API Documentation**: https://open-meteo.com/en/docs/air-quality-api
  - **Features**: PM2.5, PM10, CO, NO2, O3, European AQI

### Supporting Datasets
- **NYC Taxi Zones**: Geographic boundaries and zone mappings
- **Weather History**: Historical weather data for correlation analysis

## Technology Stack

### Data Engineering Core
- **Database**: PostgreSQL with PostGIS extension
- **Orchestration**: Apache Airflow
- **Transformation**: dbt (Data Build Tool)
- **Streaming**: Apache Kafka + Redis
- **Containerization**: Docker & Docker Compose

### Machine Learning & Analytics
- **Languages**: Python, SQL
- **ML Libraries**: TensorFlow/PyTorch, scikit-learn, Prophet
- **Geospatial**: PostGIS, GeoPandas, Folium
- **Time Series**: pandas, numpy, statsmodels

### Frontend & Visualization
- **Framework**: React + TypeScript
- **Visualization**: Plotly.js, D3.js, Mapbox
- **API**: FastAPI or Flask
- **Deployment**: Docker containers

## Success Metrics

### Data Engineering KPIs
- **Pipeline Success Rate**: >99% daily processing uptime
- **Data Quality Score**: >95% automated tests passing
- **Query Performance**: P95 <2 seconds for demand aggregations
- **Data Processing Time**: <4 hours for full refresh

### ML Performance KPIs  
- **Overall MAPE**: <20% (vs 35% historical baseline)
- **Weather Event MAPE**: <25% (vs 50% baseline)
- **Demand Surge Detection**: >80% accuracy for 2x+ normal demand
- **Prediction Lead Time**: Accurate forecasts 4+ hours ahead

### Business Impact KPIs
- **Demand Spike Prediction**: Identify weather-driven surges before they occur
- **Driver Allocation Optimization**: 15-30% improvement in wait times during weather events
- **Real-time Dashboard**: <30 second refresh for operational decisions

## Getting Started

### Prerequisites
```bash
# Install dependencies
pip -r requirements.txt

# Docker & Docker Compose
docker --version
docker-compose --version
```

## Project Status

**Current Phase**: Project Foundation & Requirements
- [x] Data source validation (taxi data + weather APIs)
- [x] Business problem definition (weather-driven demand forecasting)  
- [ ] Technology stack finalization
- [ ] Data architecture design

## Contributing

This is a learning project focused on building end-to-end data engineering and ML capabilities. The architecture is designed to be production-ready and portfolio-worthy while remaining educational and approachable.

## License

This project is for educational and portfolio purposes.