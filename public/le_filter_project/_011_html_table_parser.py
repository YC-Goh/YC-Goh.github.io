#!/usr/bin/env python3
"""
HTML Table Parser for Affix Data - OOP Implementation
Extracts table data from HTML and saves as CSV and JSON files.
"""

import csv
import json
import re
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup, Tag
import argparse


class ColumnHandler(ABC):
    """Abstract base class for column handlers."""
    
    @abstractmethod
    def extract(self, cell: Tag) -> Any:
        """Extract and process data from a table cell."""
        pass
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Clean and normalize text content."""
        if not text:
            return ""
        
        # Remove extra whitespace and newlines
        text = re.sub(r'\s+', ' ', text.strip())
        
        # Remove HTML entities
        text = text.replace('\u00a0', ' ')  # Non-breaking space
        
        return text


class NameColumnHandler(ColumnHandler):
    """Handler for the Name column - extracts affix name and descriptions."""
    
    def extract(self, cell: Tag) -> Dict[str, str]:
        """Extract name and affix type information."""
        name_parts = []
        
        # Find the main link text
        link = cell.find('a')
        if link:
            name_parts.append(self.clean_text(link.get_text()))
        
        # Look for additional descriptions - only leaf divs that are direct children
        for child in cell.children:
            if child.name == 'div':
                # Look for leaf divs within this direct child div
                leaf_divs = [div for div in child.find_all('div') if not div.find_all(['div', 'span', 'a'])]
                
                for div in leaf_divs:
                    div_text = self.clean_text(div.get_text())
                    if div_text and div_text not in name_parts:
                        # Skip metadata indicators
                        if not any(skip in div_text.lower() for skip in ['prefix', 'suffix', 'added']):
                            name_parts.append(div_text)
        
        # Combine name parts
        if len(name_parts) > 1:
            full_name = name_parts[0] + ' | ' + ' | '.join(name_parts[1:])
        else:
            full_name = name_parts[0] if name_parts else self.clean_text(cell.get_text())
        
        # Extract affix type
        affix_type = ""
        if cell.find('span', {'title': 'Prefix'}):
            affix_type = "Prefix"
        elif cell.find('span', {'title': 'Suffix'}):
            affix_type = "Suffix"
        
        return {
            'Name': full_name,
            'Affix Type': affix_type
        }


class LevelColumnHandler(ColumnHandler):
    """Handler for the Level column."""
    
    def extract(self, cell: Tag) -> str:
        """Extract level value."""
        return self.clean_text(cell.get_text())


class RerollColumnHandler(ColumnHandler):
    """Handler for the Reroll % column."""
    
    def extract(self, cell: Tag) -> str:
        """Extract reroll percentage."""
        cell_text = cell.get_text()
        percentage = re.search(r'(\d+)%', cell_text)
        return percentage.group(1) + '%' if percentage else self.clean_text(cell_text)


class TierColumnHandler(ColumnHandler):
    """Handler for tier columns (Tier1, Tier2, etc.)."""
    
    def extract(self, cell: Tag) -> str:
        """Extract tier values, handling ranges and multiple values."""
        cell_text = self.clean_text(cell.get_text())
        
        if not cell_text:
            return ""
        
        # Handle cases like "+1 (10% to 14%)" or "+(4 to 8) +1"
        if '(' in cell_text and ')' in cell_text:
            # Find all parts with their positions to preserve order
            parts_with_positions = []
            
            # Find parenthetical parts with their positions
            for match in re.finditer(r'([+-]?)\(([^)]+)\)', cell_text):
                sign, content = match.groups()
                start_pos = match.start()
                if sign:
                    part_text = f"{sign}({content})"
                else:
                    part_text = f"({content})"
                parts_with_positions.append((start_pos, part_text))
            
            # Remove parenthetical parts to find non-parenthetical content
            non_paren_text = re.sub(r'[+-]?\([^)]+\)', '', cell_text).strip()
            
            # If there's non-parenthetical content, find its position
            if non_paren_text:
                # Find where the non-paren content would be in original string
                # by looking for it before the first parenthesis
                first_paren_pos = cell_text.find('(')
                if first_paren_pos > 0 and cell_text[:first_paren_pos].strip():
                    # Content before parenthesis
                    parts_with_positions.append((0, non_paren_text))
                else:
                    # Content after parenthesis - find its approximate position
                    last_paren_pos = cell_text.rfind(')')
                    if last_paren_pos < len(cell_text) - 1:
                        parts_with_positions.append((last_paren_pos + 1, non_paren_text))
                    else:
                        # Fallback: add at end
                        parts_with_positions.append((len(cell_text), non_paren_text))
            
            # Sort by position and extract text parts
            parts_with_positions.sort(key=lambda x: x[0])
            ordered_parts = [part[1] for part in parts_with_positions]
            
            return ' | '.join(ordered_parts)
        
        return cell_text


class DefaultColumnHandler(ColumnHandler):
    """Default handler for unknown column types."""
    
    def extract(self, cell: Tag) -> str:
        """Extract raw text content."""
        return self.clean_text(cell.get_text())


class TableParser:
    """Main table parser class."""
    
    def __init__(self):
        """Initialize parser with column handlers."""
        self.column_handlers = {
            'Name': NameColumnHandler(),
            'Lvl': LevelColumnHandler(),
            'Reroll %': RerollColumnHandler(),
        }
        
        # Tier columns will be handled by TierColumnHandler
        self.tier_handler = TierColumnHandler()
        self.default_handler = DefaultColumnHandler()
    
    def _get_handler(self, column_name: str) -> ColumnHandler:
        """Get appropriate handler for a column."""
        if column_name in self.column_handlers:
            return self.column_handlers[column_name]
        elif column_name.startswith('Tier'):
            return self.tier_handler
        else:
            return self.default_handler
    
    def _extract_headers(self, table: Tag) -> List[str]:
        """Extract table headers."""
        headers = []
        header_row = table.find('thead').find('tr')
        
        for th in header_row.find_all('th'):
            header_text = ColumnHandler.clean_text(th.get_text())
            # Handle special case of "Reroll % (rarity)"
            if 'Reroll' in header_text and 'rarity' in header_text:
                header_text = 'Reroll %'
            headers.append(header_text)
        
        return headers
    
    def _extract_row_data(self, row: Tag, headers: List[str]) -> Dict[str, Any]:
        """Extract data from a single table row."""
        cells = row.find_all('td')
        if len(cells) < len(headers):
            return {}
        
        row_data = {}
        
        for i, cell in enumerate(cells):
            if i >= len(headers):
                break
            
            header = headers[i]
            handler = self._get_handler(header)
            
            # Special handling for Name column which returns multiple fields
            if header == 'Name':
                name_data = handler.extract(cell)
                row_data.update(name_data)
            else:
                row_data[header] = handler.extract(cell)
        
        return row_data
    
    def parse(self, html_content: str) -> tuple[List[Dict[str, Any]], List[str]]:
        """Parse HTML table and extract data."""
        soup = BeautifulSoup(html_content, 'html.parser')
        
        table = soup.find('table')
        if not table:
            raise ValueError("No table found in HTML content")
        
        # Extract headers
        headers = self._extract_headers(table)
        
        # Extract data rows
        data = []
        tbody = table.find('tbody')
        
        if tbody:
            for row in tbody.find_all('tr'):
                row_data = self._extract_row_data(row, headers)
                if row_data:
                    data.append(row_data)
        
        return data, headers


class DataExporter:
    """Handles data export to different formats."""
    
    @staticmethod
    def _get_ordered_fieldnames(data: List[Dict[str, Any]]) -> List[str]:
        """Get ordered field names with priority fields first."""
        if not data:
            return []
        
        # Get all unique keys
        all_keys = set()
        for record in data:
            all_keys.update(record.keys())
        
        # Define priority order
        priority_fields = ['Name', 'Affix Type', 'Lvl', 'Reroll %']
        ordered_fieldnames = []
        
        # Add priority fields first
        for field in priority_fields:
            if field in all_keys:
                ordered_fieldnames.append(field)
                all_keys.remove(field)
        
        # Add remaining fields in sorted order
        ordered_fieldnames.extend(sorted(all_keys))
        
        return ordered_fieldnames
    
    @staticmethod
    def save_csv(data: List[Dict[str, Any]], filename: str) -> None:
        """Save data as CSV file."""
        if not data:
            print("No data to save")
            return
        
        fieldnames = DataExporter._get_ordered_fieldnames(data)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
        
        print(f"Data saved as CSV: {filename}")
    
    @staticmethod
    def save_json(data: List[Dict[str, Any]], filename: str) -> None:
        """Save data as JSON file."""
        with open(filename, 'w', encoding='utf-8') as jsonfile:
            json.dump(data, jsonfile, indent=2, ensure_ascii=False)
        
        print(f"Data saved as JSON: {filename}")


class HTMLTableProcessor:
    """Main processor class that orchestrates the parsing and exporting."""
    
    def __init__(self):
        """Initialize processor with parser and exporter."""
        self.parser = TableParser()
        self.exporter = DataExporter()
    
    def process_file(self, input_file: str, output_base_name: Optional[str] = None,
                    csv_only: bool = False, json_only: bool = False) -> None:
        """Process a single HTML file."""
        input_path = Path(input_file)
        
        if not input_path.exists():
            print(f"Error: File {input_file} not found")
            return
        
        # Determine output base name
        if output_base_name is None:
            output_base_name = input_path.stem
        
        try:
            # Read HTML content
            with open(input_path, 'r', encoding='utf-8') as f:
                html_content = f.read()
            
            # Parse the table
            data, headers = self.parser.parse(html_content)
            
            if not data:
                print(f"No data extracted from {input_file}")
                return
            
            print(f"Extracted {len(data)} rows with headers: {headers}")
            
            # Export data
            if not json_only:
                csv_filename = f"{output_base_name}.csv"
                self.exporter.save_csv(data, csv_filename)
            
            if not csv_only:
                json_filename = f"{output_base_name}.json"
                self.exporter.save_json(data, json_filename)
                
        except Exception as e:
            print(f"Error processing {input_file}: {e}")
    
    def process_files(self, input_files: List[str], output_base: Optional[str] = None,
                     csv_only: bool = False, json_only: bool = False) -> None:
        """Process multiple HTML files."""
        for input_file in input_files:
            print(f"\nProcessing: {input_file}")
            
            # Determine output name for multiple files
            output_name = output_base
            if len(input_files) > 1 and output_base:
                base_name = Path(input_file).stem
                output_name = f"{output_base}_{base_name}"
            
            self.process_file(input_file, output_name, csv_only, json_only)


def main():
    """Main function with command line interface."""
    parser = argparse.ArgumentParser(description='Extract table data from HTML files')
    parser.add_argument('input_files', nargs='+', help='HTML files to process')
    parser.add_argument('-o', '--output', help='Output base name (default: use input filename)')
    parser.add_argument('--csv-only', action='store_true', help='Only output CSV format')
    parser.add_argument('--json-only', action='store_true', help='Only output JSON format')
    
    args = parser.parse_args()
    
    # Create processor and run
    processor = HTMLTableProcessor()
    processor.process_files(
        args.input_files,
        args.output,
        args.csv_only,
        args.json_only
    )


if __name__ == "__main__":
    # If no command line arguments, provide example usage
    import sys
    if len(sys.argv) == 1:
        print("HTML Table Parser - Extract affix data from HTML tables")
        print("\nUsage examples:")
        print("  python script.py affix_details_snippet.html")
        print("  python script.py *.html")
        print("  python script.py table1.html table2.html -o combined_output")
        print("  python script.py data.html --csv-only")
        print("\nFor help: python script.py -h")
        
        # Try to process the example file if it exists
        example_file = "affix_details_snippet.html"
        if Path(example_file).exists():
            print(f"\nFound {example_file}, processing as example...")
            processor = HTMLTableProcessor()
            processor.process_file(example_file)
        else:
            print(f"\nTo test with your file, run:")
            print(f"  python script.py your_file.html")
    else:
        main()
