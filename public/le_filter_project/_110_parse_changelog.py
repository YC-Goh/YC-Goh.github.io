#!/usr/bin/env python3
"""
Changelog Generator Script
Processes filter_maker.yml and generates markdown files for each sub-release.
"""

import yaml
import os
from pathlib import Path

def load_yaml_file(filepath):
    """Load and parse the YAML file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"Error: Could not find file {filepath}")
        return None
    except yaml.YAMLError as e:
        print(f"Error parsing YAML: {e}")
        return None

def create_markdown_content(version, release_data, sub_releases_up_to_index):
    """Generate markdown content for a specific sub-release."""
    description = release_data.get('description', '').strip()
    sub_releases = release_data.get('sub_releases', [])
    
    # Create the markdown content
    content = f"#   Release {version}\n\n"
    content += f"{description}\n\n"
    content += "##  Sub-releases\n\n"
    content += "| Version | Notes |\n"
    content += "|---------|-------|\n"
    
    # Add sub-releases up to the current index
    for i in range(sub_releases_up_to_index + 1):
        if i < len(sub_releases):
            sub_release = sub_releases[i]
            # Extract version and description from the sub-release entry
            for sub_version, sub_description in sub_release.items():
                content += f"| {sub_version} | {sub_description} |\n"
    
    return content

def generate_changelog_files(yaml_filepath, output_dir):
    """Main function to generate changelog markdown files."""
    # Load the YAML data
    data = load_yaml_file(yaml_filepath)
    if not data:
        return
    
    # Ensure output directory exists
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    # Process each main release
    for main_version, release_data in data.items():
        sub_releases = release_data.get('sub_releases', [])
        
        # Generate a markdown file for each sub-release
        for i, sub_release in enumerate(sub_releases):
            for sub_version, sub_description in sub_release.items():
                # Generate markdown content
                markdown_content = create_markdown_content(
                    main_version, 
                    release_data, 
                    i  # Include sub-releases up to current index
                )
                
                # Create filename
                filename = f"filter.maker.{sub_version}.md"
                filepath = os.path.join(output_dir, filename)
                
                # Write the markdown file
                try:
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(markdown_content)
                    print(f"Generated: {filepath}")
                except IOError as e:
                    print(f"Error writing file {filepath}: {e}")

def main():
    """Main execution function."""
    # Define paths
    yaml_file = os.path.join('changelog', 'filter_maker.yml')
    output_dir = 'changelog'
    
    print("Changelog Generator")
    print("=" * 50)
    print(f"Reading from: {yaml_file}")
    print(f"Output directory: {output_dir}")
    print()
    
    # Check if YAML file exists
    if not os.path.exists(yaml_file):
        print(f"Error: YAML file not found at {yaml_file}")
        print("Please ensure the file exists in the changelog subfolder.")
        return
    
    # Generate the changelog files
    generate_changelog_files(yaml_file, output_dir)
    print("\nChangelog generation complete!")

if __name__ == "__main__":
    main()