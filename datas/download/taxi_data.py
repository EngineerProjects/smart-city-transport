#!/usr/bin/env python3
"""
NYC TLC Taxi Trip Data Downloader - Monthly Files Only
Download all types of NYC taxi data: Yellow, Green, FHV, FHVHV
"""

import os
import requests
from pathlib import Path
import argparse
from tqdm import tqdm

class NYCTaxiDownloader:
    def __init__(self, base_dir="data"):
        self.base_url = "https://d37ci6vzurychx.cloudfront.net/trip-data"
        self.base_dir = Path(base_dir)
        
        # Data type configurations
        self.data_types = {
            'yellow': {
                'prefix': 'yellow_tripdata',
                'description': 'Yellow Taxi (Manhattan pickups)',
                'start_year': 2009
            },
            'green': {
                'prefix': 'green_tripdata', 
                'description': 'Green Taxi (Outer boroughs)',
                'start_year': 2013
            },
            'fhv': {
                'prefix': 'fhv_tripdata',
                'description': 'For-Hire Vehicles',
                'start_year': 2015
            },
            'fhvhv': {
                'prefix': 'fhvhv_tripdata',
                'description': 'High Volume FHV (Uber/Lyft)',
                'start_year': 2019
            }
        }

    def download_file(self, url, filepath):
        """Download file with progress bar"""
        try:
            response = requests.get(url, stream=True)
            response.raise_for_status()
            
            total_size = int(response.headers.get('content-length', 0))
            
            # Create directory if it doesn't exist
            os.makedirs(filepath.parent, exist_ok=True)
            
            with open(filepath, 'wb') as file, tqdm(
                desc=filepath.name,
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
                    pbar.update(len(chunk))
            
            return True
            
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return False

    def file_exists_and_valid(self, filepath):
        """Check if file exists and is not empty"""
        return filepath.exists() and filepath.stat().st_size > 0

    def download_data_type(self, data_type, years, months):
        """Download specific data type for given years/months"""
        
        if data_type not in self.data_types:
            print(f"Unknown data type: {data_type}")
            return
        
        config = self.data_types[data_type]
        data_dir = self.base_dir / f"{data_type}_trip"
        
        print(f"Downloading {config['description']} data...")
        print(f"Directory: {data_dir}")
        print(f"Format: Monthly files only")
        
        downloaded_count = 0
        skipped_count = 0
        failed_count = 0
        
        for year in years:
            # Skip years before data availability
            if year < config['start_year']:
                print(f"Skipping {year} - {data_type} data starts from {config['start_year']}")
                continue
                
            for month in months:
                filename = f"{config['prefix']}_{year}-{month:02d}.parquet"
                url = f"{self.base_url}/{filename}"
                filepath = data_dir / filename
                
                if self.file_exists_and_valid(filepath):
                    print(f"Skipping {filename} - already exists")
                    skipped_count += 1
                    continue
                
                if self.download_file(url, filepath):
                    downloaded_count += 1
                else:
                    failed_count += 1
        
        print(f"{data_type.upper()} Summary:")
        print(f"  Downloaded: {downloaded_count} files")
        print(f"  Skipped: {skipped_count} files")
        print(f"  Failed: {failed_count} files")

    def list_available_data(self):
        """Display information about available data types"""
        print("Available NYC TLC Data Types:")
        print("-" * 50)
        
        for key, config in self.data_types.items():
            print(f"{key.upper()}:")
            print(f"  Description: {config['description']}")
            print(f"  Available from: {config['start_year']}")
            print(f"  File pattern: {config['prefix']}_YYYY-MM.parquet")
            print()

    def estimate_download_size(self, data_types, years, months):
        """Estimate total download size"""
        total_files = 0
        
        for data_type in data_types:
            if data_type in self.data_types:
                valid_years = [y for y in years if y >= self.data_types[data_type]['start_year']]
                total_files += len(valid_years) * len(months)
        
        # Average file size is approximately 60MB
        estimated_size_gb = (total_files * 60) / 1024
        
        print(f"Estimated download:")
        print(f"  Files: {total_files}")
        print(f"  Size: ~{estimated_size_gb:.1f} GB")

def main():
    parser = argparse.ArgumentParser(description='Download NYC TLC Trip Data (Monthly Files)')
    
    # Data type selection
    parser.add_argument('--types', nargs='+', 
                        choices=['yellow', 'green', 'fhv', 'fhvhv', 'all'],
                        default=['yellow'],
                        help='Data types to download (default: yellow)')
    
    # Time range
    parser.add_argument('--years', nargs='+', type=int, 
                        default=[2023, 2024, 2025],
                        help='Years to download (default: 2023 2024 2025)')
    
    parser.add_argument('--months', nargs='+', type=int, 
                        default=list(range(1, 13)),
                        help='Months to download (default: all months)')
    
    # Directory
    parser.add_argument('--data-dir', default='data',
                        help='Base directory for data storage (default: data)')
    
    # Actions
    parser.add_argument('--list', action='store_true',
                        help='List available data types and exit')
    
    parser.add_argument('--estimate', action='store_true',
                        help='Estimate download size and exit')
    
    args = parser.parse_args()
    
    downloader = NYCTaxiDownloader(args.data_dir)
    
    if args.list:
        downloader.list_available_data()
        return
    
    # Handle 'all' option
    if 'all' in args.types:
        data_types = ['yellow', 'green', 'fhv', 'fhvhv']
    else:
        data_types = args.types
    
    if args.estimate:
        downloader.estimate_download_size(data_types, args.years, args.months)
        return
    
    print(f"NYC TLC Data Downloader - Monthly Files Only")
    print(f"Data types: {', '.join(data_types)}")
    print(f"Years: {args.years}")
    print(f"Months: {args.months}")
    print(f"Base directory: {args.data_dir}")
    
    # Estimate and confirm
    downloader.estimate_download_size(data_types, args.years, args.months)
    
    confirm = input("\nContinue with download? (y/N): ")
    if confirm.lower() != 'y':
        print("Download cancelled.")
        return
    
    # Download each data type
    for data_type in data_types:
        downloader.download_data_type(data_type, args.years, args.months)
    
    print("All downloads complete!")

if __name__ == "__main__":
    main()