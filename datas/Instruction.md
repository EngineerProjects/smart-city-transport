# Data Download Instructions

## File Structure Overview

After following these instructions, your data directory will look like this:

```
data/
├── nyc_taxi_mapping/          # Zone mapping files
│   ├── taxi_zone_lookup.csv   # Zone ID to name/borough mapping
│   ├── taxi_zones.zip         # Original shapefile ZIP
│   └── shapefiles/            # Extracted shapefile components
│       ├── taxi_zones.shp     # Main shapefile
│       ├── taxi_zones.dbf     # Attribute data
│       ├── taxi_zones.shx     # Shape index
│       └── taxi_zones.prj     # Projection info
└── yellow_trip/               # Taxi trip data (monthly files)
    ├── yellow_tripdata_2023-01.parquet
    ├── yellow_tripdata_2023-02.parquet
    └── ... (one file per month)
```

## Step 1: Download NYC Taxi Zone Mapping Data

This data maps Zone IDs from trip records to geographic coordinates and zone names.

### Basic Download (Recommended)
```bash
python3 datas/download/nyc_taxi_mapping.py
```

When prompted, choose option **1** (Essential files only).

### Alternative Commands
```bash
# Download all available files (includes zone maps)
python3 datas/download/nyc_taxi_mapping.py --all

# List available files without downloading
python3 datas/download/nyc_taxi_mapping.py --list

# Verify existing downloads
python3 datas/download/nyc_taxi_mapping.py --verify
```

### Expected Output
```
Downloading essential NYC taxi mapping files...
This will download:
1. Taxi Zone Lookup CSV - Zone ID to coordinates mapping
2. Taxi Zone Shapefile (ZIP) - Geographic boundaries
```

The script will:
1. Download `taxi_zone_lookup.csv` (12KB)
2. Download `taxi_zones.zip` (shapefile archive)
3. Automatically extract the ZIP to `shapefiles/` folder

## Step 2: Download NYC Taxi Trip Data

### Basic Download (3 Years of Yellow Taxi Data)
```bash
python3 datas/download/taxi_data.py --types yellow --years 2023 2024 2025
```

### Download Specific Data Types
```bash
# Download yellow and green taxi data
python3 datas/download/taxi_data.py --types yellow green --years 2023 2024 2025

# Download all taxi types
python3 datas/download/taxi_data.py --types all --years 2024 2025

# Download specific months only
python3 datas/download/taxi_data.py --types yellow --years 2024 --months 1 2 3 6 9 12
```

### Available Data Types
- **yellow**: Yellow Taxi (Manhattan pickups) - Available from 2009
- **green**: Green Taxi (Outer boroughs) - Available from 2013  
- **fhv**: For-Hire Vehicles - Available from 2015
- **fhvhv**: High Volume FHV (Uber/Lyft) - Available from 2019

### Check Before Downloading
```bash
# See available data types
python3 datas/download/taxi_data.py --list

# Estimate download size
python3 datas/download/taxi_data.py --types yellow --years 2023 2024 2025 --estimate
```

### Expected Download Sizes
- **1 month of yellow taxi data**: ~60MB
- **1 year of yellow taxi data**: ~720MB  
- **3 years of yellow taxi data**: ~2.2GB

## Step 3: Verify Downloads

### Check Taxi Zone Mapping
```bash
python3 datas/download/nyc_taxi_mapping.py --verify
```

### Check Downloaded Trip Data
```bash
# List files in the data directory
ls -la data/yellow_trip/

# Count downloaded files
ls data/yellow_trip/ | wc -l
```

### Test Data Loading
```bash
python3 datas/read.py
```

## Common Download Scenarios

### Scenario 1: First Time Setup (Minimal)
```bash
# Download zone mapping
python3 datas/download/nyc_taxi_mapping.py
# Choose option 1

# Download 1 year of yellow taxi data
python3 datas/download/taxi_data.py --types yellow --years 2024
```

### Scenario 2: Full Dataset for Analysis
```bash
# Download zone mapping
python3 datas/download/nyc_taxi_mapping.py

# Download 3 years of yellow taxi data
python3 datas/download/taxi_data.py --types yellow --years 2023 2024 2025
```

### Scenario 3: Multi-Modal Transportation Study
```bash
# Download zone mapping
python3 datas/download/nyc_taxi_mapping.py

# Download multiple taxi types
python3 datas/download/taxi_data.py --types yellow green fhvhv --years 2024 2025
```

## Troubleshooting

### Download Failures
If downloads fail:
1. Check internet connection
2. Some files may be temporarily unavailable - try again later
3. Check if you have sufficient disk space

### Large Downloads
For large downloads (multiple years/types):
1. Downloads can take 10-60 minutes depending on connection speed
2. Files are downloaded with progress bars
3. Existing files are automatically skipped
4. Downloads can be resumed if interrupted

