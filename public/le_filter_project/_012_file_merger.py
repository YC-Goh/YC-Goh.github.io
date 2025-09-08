#!/usr/bin/env python3
"""
File merger utility for CSV and JSON files.
Combines multiple CSV files into one CSV and multiple JSON files into one JSON.
"""

import csv
import json
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd


class FileMerger:
    """Utility class for merging CSV and JSON files."""
    
    @staticmethod
    def merge_csv_files(csv_files: List[str], output_file: str, add_source_column: bool = True) -> bool:
        """
        Merge multiple CSV files into a single CSV file.
        
        Args:
            csv_files: List of CSV file paths to merge
            output_file: Output CSV file path
            add_source_column: Whether to add a 'Source File' column
            
        Returns:
            True if successful, False otherwise
        """
        try:
            all_data = []
            all_fieldnames = set()
            
            # First pass: collect all unique fieldnames
            for csv_file in csv_files:
                csv_path = Path(csv_file)
                if not csv_path.exists():
                    print(f"  ⚠️  CSV file not found: {csv_file}")
                    continue
                    
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    all_fieldnames.update(reader.fieldnames or [])
            
            # Convert to sorted list, with Source File at the end if added
            ordered_fieldnames = sorted(all_fieldnames)
            if add_source_column and 'Source File' not in ordered_fieldnames:
                ordered_fieldnames.append('Source File')
            
            # Second pass: read all data
            for csv_file in csv_files:
                csv_path = Path(csv_file)
                if not csv_path.exists():
                    continue
                    
                with open(csv_path, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        # Fill missing columns with empty strings
                        complete_row = {field: row.get(field, '') for field in ordered_fieldnames}
                        
                        # Add source file info if requested
                        if add_source_column:
                            complete_row['Source File'] = csv_path.stem
                            
                        all_data.append(complete_row)
            
            # Write combined CSV
            if all_data:
                with open(output_file, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=ordered_fieldnames)
                    writer.writeheader()
                    writer.writerows(all_data)
                
                print(f"  ✅ Merged {len(csv_files)} CSV files into: {output_file}")
                print(f"     Total rows: {len(all_data)}")
                return True
            else:
                print(f"  ⚠️  No data found in CSV files")
                return False
                
        except Exception as e:
            print(f"  ❌ Error merging CSV files: {e}")
            return False
    
    @staticmethod
    def merge_json_files(json_files: List[str], output_file: str, add_source_field: bool = True) -> bool:
        """
        Merge multiple JSON files into a single JSON file.
        
        Args:
            json_files: List of JSON file paths to merge
            output_file: Output JSON file path
            add_source_field: Whether to add a 'source_file' field to each record
            
        Returns:
            True if successful, False otherwise
        """
        try:
            all_data = []
            
            for json_file in json_files:
                json_path = Path(json_file)
                if not json_path.exists():
                    print(f"  ⚠️  JSON file not found: {json_file}")
                    continue
                    
                with open(json_path, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        
                        # Handle both single objects and arrays
                        if isinstance(data, list):
                            file_data = data
                        else:
                            file_data = [data]
                        
                        # Add source file info if requested
                        if add_source_field:
                            for record in file_data:
                                if isinstance(record, dict):
                                    record['source_file'] = json_path.stem
                        
                        all_data.extend(file_data)
                        
                    except json.JSONDecodeError as e:
                        print(f"  ⚠️  Invalid JSON in {json_file}: {e}")
                        continue
            
            # Write combined JSON
            if all_data:
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(all_data, f, indent=2, ensure_ascii=False)
                
                print(f"  ✅ Merged {len(json_files)} JSON files into: {output_file}")
                print(f"     Total records: {len(all_data)}")
                return True
            else:
                print(f"  ⚠️  No data found in JSON files")
                return False
                
        except Exception as e:
            print(f"  ❌ Error merging JSON files: {e}")
            return False
    
    @staticmethod
    def merge_files_in_directory(directory: str, output_prefix: str = "merged", 
                                add_source_info: bool = True) -> tuple[bool, bool]:
        """
        Merge all CSV and JSON files in a directory.
        
        Args:
            directory: Directory containing files to merge
            output_prefix: Prefix for output filenames
            add_source_info: Whether to add source file information
            
        Returns:
            Tuple of (csv_success, json_success)
        """
        dir_path = Path(directory)
        
        if not dir_path.exists() or not dir_path.is_dir():
            print(f"❌ Directory not found: {directory}")
            return False, False
        
        # Find all CSV and JSON files
        csv_files = list(dir_path.glob("*.csv"))
        json_files = list(dir_path.glob("*.json"))
        
        print(f"📂 Found {len(csv_files)} CSV files and {len(json_files)} JSON files in {directory}")
        
        csv_success = True
        json_success = True
        
        # Merge CSV files
        if csv_files:
            csv_output = dir_path / f"{output_prefix}.csv"
            csv_success = FileMerger.merge_csv_files(
                [str(f) for f in csv_files], 
                str(csv_output), 
                add_source_info
            )
        else:
            print("  📄 No CSV files to merge")
        
        # Merge JSON files
        if json_files:
            json_output = dir_path / f"{output_prefix}.json"
            json_success = FileMerger.merge_json_files(
                [str(f) for f in json_files], 
                str(json_output), 
                add_source_info
            )
        else:
            print("  📄 No JSON files to merge")
        
        return csv_success, json_success


def main():
    """Example usage of the FileMerger."""
    import sys
    
    if len(sys.argv) < 2:
        print("File Merger - Combine CSV and JSON files")
        print("\nUsage examples:")
        print("  python file_merger.py /path/to/files")
        print("  python file_merger.py /path/to/files --output-prefix combined_data")
        print("  python file_merger.py /path/to/files --no-source-info")
        return
    
    directory = sys.argv[1]
    output_prefix = "merged"
    add_source_info = True
    
    # Parse optional arguments
    if "--output-prefix" in sys.argv:
        idx = sys.argv.index("--output-prefix")
        if idx + 1 < len(sys.argv):
            output_prefix = sys.argv[idx + 1]
    
    if "--no-source-info" in sys.argv:
        add_source_info = False
    
    print(f"🔄 Merging files in: {directory}")
    print(f"📝 Output prefix: {output_prefix}")
    print(f"🏷️  Add source info: {add_source_info}")
    print("-" * 50)
    
    csv_success, json_success = FileMerger.merge_files_in_directory(
        directory, output_prefix, add_source_info
    )
    
    print("\n" + "=" * 50)
    print("MERGE SUMMARY")
    print("=" * 50)
    print(f"CSV merge: {'✅ Success' if csv_success else '❌ Failed'}")
    print(f"JSON merge: {'✅ Success' if json_success else '❌ Failed'}")


if __name__ == "__main__":
    main()
