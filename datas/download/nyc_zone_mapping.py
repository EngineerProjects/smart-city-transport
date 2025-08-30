#!/usr/bin/env python3
"""
NYC Taxi Zone Mapping Data Downloader
Download taxi zone lookup tables, shapefiles, and zone maps
"""

import os
import requests
import zipfile
from pathlib import Path
import argparse
from tqdm import tqdm

class NYCMappingDownloader:
    def __init__(self, base_dir="data"):
        self.base_dir = Path(base_dir) / "nyc_taxi_mapping"
        
        # Data sources based on TLC official documentation
        self.data_sources = {
            'zone_lookup': {
                'url': 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv',
                'filename': 'taxi_zone_lookup.csv',
                'description': 'Taxi Zone ID to Borough/Zone name mapping'
            },
            'zone_shapefile': {
                'url': 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zones.zip',
                'filename': 'taxi_zones.zip',
                'description': 'Taxi Zone boundaries shapefile (ZIP archive)'
            },
            'zone_map_manhattan': {
                'url': 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_map_manhattan.jpg',
                'filename': 'taxi_zone_map_manhattan.jpg',
                'description': 'Manhattan taxi zones map'
            },
            'zone_map_brooklyn': {
                'url': 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_map_brooklyn.jpg', 
                'filename': 'taxi_zone_map_brooklyn.jpg',
                'description': 'Brooklyn taxi zones map'
            },
            'zone_map_queens': {
                'url': 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_map_queens.jpg',
                'filename': 'taxi_zone_map_queens.jpg', 
                'description': 'Queens taxi zones map'
            },
            'zone_map_bronx': {
                'url': 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_map_bronx.jpg',
                'filename': 'taxi_zone_map_bronx.jpg',
                'description': 'Bronx taxi zones map'
            },
            'zone_map_staten_island': {
                'url': 'https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_map_staten_island.jpg',
                'filename': 'taxi_zone_map_staten_island.jpg',
                'description': 'Staten Island taxi zones map'
            }
        }

    def download_file(self, url, filepath, description=""):
        """Download file with progress bar"""
        try:
            print(f"Downloading: {description}")
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
            
            print(f"Saved: {filepath}")
            return True
            
        except requests.RequestException as e:
            print(f"Error downloading {url}: {e}")
            return False

    def file_exists_and_valid(self, filepath):
        """Check if file exists and is not empty"""
        return filepath.exists() and filepath.stat().st_size > 0

    def extract_shapefile(self, zip_filepath):
        """Extract shapefile from ZIP archive"""
        try:
            extract_dir = zip_filepath.parent / "shapefiles"
            
            print(f"Extracting {zip_filepath.name}...")
            with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # List extracted files
            extracted_files = list(extract_dir.glob("*"))
            print(f"Extracted {len(extracted_files)} files to {extract_dir}")
            for file in extracted_files:
                print(f"  - {file.name}")
                
            return True
            
        except Exception as e:
            print(f"Error extracting shapefile: {e}")
            return False

    def download_essential_files(self):
        """Download only the essential files for coordinate mapping"""
        essential_files = ['zone_lookup', 'zone_shapefile']
        
        print("Downloading essential NYC taxi mapping files...")
        print("This will download:")
        print("1. Taxi Zone Lookup CSV - Zone ID to coordinates mapping")  
        print("2. Taxi Zone Shapefile (ZIP) - Geographic boundaries")
        
        success_count = 0
        
        for key in essential_files:
            source = self.data_sources[key]
            filepath = self.base_dir / source['filename']
            
            if self.file_exists_and_valid(filepath):
                print(f"Skipping {source['filename']} - already exists")
                success_count += 1
                continue
            
            if self.download_file(source['url'], filepath, source['description']):
                success_count += 1
                
                # Extract shapefile if it's a ZIP file
                if source['filename'] == 'taxi_zones.zip':
                    self.extract_shapefile(filepath)
        
        return success_count == len(essential_files)

    def download_all_files(self):
        """Download all available mapping files"""
        print("Downloading all NYC taxi mapping files...")
        
        success_count = 0
        total_files = len(self.data_sources)
        
        for key, source in self.data_sources.items():
            filepath = self.base_dir / source['filename']
            
            if self.file_exists_and_valid(filepath):
                print(f"Skipping {source['filename']} - already exists")
                success_count += 1
                continue
            
            if self.download_file(source['url'], filepath, source['description']):
                success_count += 1
                
                # Extract shapefile if it's a ZIP file
                if source['filename'] == 'taxi_zones.zip':
                    self.extract_shapefile(filepath)
        
        print(f"Download summary: {success_count}/{total_files} files successful")
        return success_count == total_files

    def list_available_files(self):
        """Display information about available files"""
        print("Available NYC Taxi Zone Mapping Files:")
        print("-" * 60)
        
        print("ESSENTIAL FILES (recommended for coordinate mapping):")
        essential = ['zone_lookup', 'zone_shapefile']
        for key in essential:
            source = self.data_sources[key]
            print(f"  {source['filename']}")
            print(f"    Description: {source['description']}")
            print(f"    URL: {source['url']}")
            print()

    def verify_downloads(self):
        """Verify downloaded files and provide usage information"""
        print("Verifying downloaded files...")
        
        essential_files = {
            'taxi_zone_lookup.csv': 'Zone ID to name mapping',
            'taxi_zones.zip': 'Geographic boundaries shapefile',
            'shapefiles/': 'Extracted shapefile directory'
        }
        
        all_good = True
        
        for filename, description in essential_files.items():
            if filename.endswith('/'):
                # Check for directory
                dirpath = self.base_dir / filename.rstrip('/')
                if dirpath.exists() and dirpath.is_dir():
                    file_count = len(list(dirpath.glob('*')))
                    print(f"✓ {filename} ({file_count} files) - {description}")
                else:
                    print(f"✗ {filename} - Missing directory")
                    all_good = False
            else:
                filepath = self.base_dir / filename
                if self.file_exists_and_valid(filepath):
                    size_kb = filepath.stat().st_size / 1024
                    print(f"✓ {filename} ({size_kb:.1f} KB) - {description}")
                else:
                    print(f"✗ {filename} - Missing or empty")
                    all_good = False
        
        if all_good:
            print("\nAll essential files downloaded successfully!")
        else:
            print("\nSome files are missing. Please re-run the download.")

def main():
    parser = argparse.ArgumentParser(description='Download NYC Taxi Zone Mapping Data')
    
    # Download options
    parser.add_argument('--essential-only', action='store_true',
                        help='Download only essential files (lookup CSV + shapefile)')
    
    parser.add_argument('--all', action='store_true',
                        help='Download all available files (lookup, shapefiles, maps)')
    
    # Directory
    parser.add_argument('--data-dir', default='data',
                        help='Base directory for data storage (default: data)')
    
    # Actions
    parser.add_argument('--list', action='store_true',
                        help='List available files and exit')
    
    parser.add_argument('--verify', action='store_true',
                        help='Verify existing downloads and show usage info')
    
    args = parser.parse_args()
    
    downloader = NYCMappingDownloader(args.data_dir)
    
    if args.list:
        downloader.list_available_files()
        return
    
    if args.verify:
        downloader.verify_downloads()
        return
    
    print("NYC Taxi Zone Mapping Downloader")
    print(f"Download directory: {downloader.base_dir}")
    
    # Determine download mode
    if args.all:
        print("Mode: Download all files")
        success = downloader.download_all_files()
    elif args.essential_only:
        print("Mode: Download essential files only")
        success = downloader.download_essential_files()
    else:
        # Ask user what they want
        print("What would you like to download?")
        print("1. Essential files only (lookup CSV + shapefile) - Recommended")
        print("2. All files (lookup + shapefiles + zone maps)")
        
        while True:
            choice = input("Choose option (1 or 2): ").strip()
            if choice == '1':
                success = downloader.download_essential_files()
                break
            elif choice == '2':
                success = downloader.download_all_files()
                break
            else:
                print("Please enter 1 or 2")
    
    if success:
        print("\nDownload completed successfully!")
        downloader.verify_downloads()
    else:
        print("\nSome downloads failed. Please check your internet connection and try again.")

if __name__ == "__main__":
    main()