#!/usr/bin/env python3
"""
Batch processor for HTML table files.
Processes multiple HTML files using the HTMLTableProcessor.
"""

import sys
from pathlib import Path

# Import the main processor (assumes the OOP script is in the same directory)
try:
    from _011_html_table_parser import HTMLTableProcessor
except ImportError:
    print("Error: Could not import HTMLTableProcessor.")
    print("Make sure the main parser script is named 'html_table_parser.py' and in the same directory.")
    sys.exit(1)

# Import the file merger (assumes the OOP script is in the same directory)
try:
    from _012_file_merger import FileMerger
except ImportError:
    print("Error: Could not import FileMerger.")
    print("Make sure the file_merger script is named 'file_merger.py' and in the same directory.")
    sys.exit(1)


def main():
    """Process multiple HTML files in batch."""
    
    # ===== CONFIGURE YOUR FILES HERE =====
    files_to_process = [
        "affix_details_1.html", 
        "affix_details_2.html", 
        "affix_details_3.html", 
        "affix_details_4.html", 
        "affix_details_5.html", 
        # "affix_details_6.html", 
        # "affix_details_i1.html", 
        # "affix_details_i2.html", 
        # "affix_details_i3.html", 
        # "affix_details_i4.html", 
        # "affix_details_i5.html", 
        # "affix_details_i6.html", 
        # Add or modify filenames as needed
    ]

    # Input folder (where HTML files are located)
    input_folder = "./affix_id/idol/raw"  # or "." for current directory
    input_path = Path(input_folder)
    files_to_process = list(map(input_path.joinpath, files_to_process))

    # Output folder (where CSV/JSON files will be saved)  
    output_folder = "./affix_id/idol/processed"  # or "." for current directory
    output_path = Path(output_folder)
    
    # Optional: Set a common output prefix (leave as None to use individual filenames)
    output_prefix = None  # e.g., "affix_data" would create "affix_data_table1.csv", etc.
    
    # Output format options
    csv_only = False    # Set to True if you only want CSV files
    json_only = False   # Set to True if you only want JSON files

    # New merge options in the batch processor
    merge_files = True              # Set to False to skip merging
    merged_filename = "all_data"    # Base name for merged files
    add_source_info = True          # Add source filename to each record
    # =====================================
    
    
    print(f"Batch HTML Table Processor")
    print(f"Processing {len(files_to_process)} files...")
    print("-" * 50)
    
    # Initialize processor
    processor = HTMLTableProcessor()
    
    # Track results
    successful = 0
    failed = 0
    missing = 0
    
    # Process each file
    for i, filename in enumerate(files_to_process, 1):
        print(f"\n[{i}/{len(files_to_process)}] Processing: {filename}")
        
        # Check if file exists
        if not Path(filename).exists():
            print(f"  ❌ File not found: {filename}")
            missing += 1
            continue
        
        try:
            # Determine output name
            base_name = Path(filename).stem
            if output_prefix and len(files_to_process) > 1:
                output_name = f"{output_prefix}_{base_name}"
            else:
                output_name = base_name
            output_name = output_path.joinpath(output_name)
            
            # Process the file
            processor.process_file(
                filename, 
                output_name, 
                csv_only=csv_only, 
                json_only=json_only
            )
            print(f"  ✅ Success!")
            successful += 1
            
        except Exception as e:
            print(f"  ❌ Error: {e}")
            failed += 1
    
    # Print summary
    print("\n" + "=" * 60)
    print("BATCH PROCESSING SUMMARY")
    print("=" * 60)
    print(f"📁 Input folder: {input_path.absolute()}")
    print(f"📁 Output folder: {output_path.absolute()}")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📄 Missing files: {missing}")
    print(f"📊 Total attempted: {len(files_to_process)}")
    
    if successful > 0:
        print(f"\n🎉 Successfully processed {successful} files!")
        if not csv_only and not json_only:
            print(f"Generated {successful * 2} output files (CSV + JSON)")
        else:
            print(f"Generated {successful} output files")
        print(f"📂 Check output folder: {output_path.absolute()}")
        
        # Merge files if requested
        if merge_files and successful > 1:
            print(f"\n🔄 Merging files...")
            print("-" * 40)
            
            merger = FileMerger()
            csv_success, json_success = merger.merge_files_in_directory(
                str(output_path), 
                merged_filename, 
                add_source_info
            )
            
            print("\n" + "=" * 40)
            print("MERGE RESULTS")
            print("=" * 40)
            if not json_only:
                print(f"CSV merge: {'✅ Success' if csv_success else '❌ Failed'}")
            if not csv_only:
                print(f"JSON merge: {'✅ Success' if json_success else '❌ Failed'}")
            
            if csv_success or json_success:
                print(f"🎯 Merged files available in: {output_path.absolute()}")
        elif successful == 1:
            print("📝 Only one file processed - no merging needed")
        elif not merge_files:
            print("📝 File merging disabled")


if __name__ == "__main__":
    main()