import json
import csv
import os
import argparse
from collections import Counter, defaultdict

def stream_json_array(file_path):
    """Generator to yield JSON objects from a large top-level JSON array."""
    with open(file_path, 'r', encoding='utf-8') as f:
        buffer = ''
        depth = 0
        in_string = False
        escape = False
        array_started = False

        while True:
            char = f.read(1)
            if not char:
                break

            if not array_started:
                if char in '[ \n\r\t':
                    if char == '[':
                        array_started = True
                    continue

            buffer += char

            # Handle string escape sequences
            if char == '"' and not escape:
                in_string = not in_string
            if char == '\\' and not escape:
                escape = True
                continue
            escape = False

            # Count braces only outside strings
            if not in_string:
                if char == '{':
                    depth += 1
                elif char == '}':
                    depth -= 1

            # Complete JSON object found
            if depth == 0 and buffer.strip():
                obj_str = buffer.strip()
                # Ignore a closing bracket of the array
                if obj_str == ']':
                    break
                # Remove trailing comma if present
                if obj_str.endswith(','):
                    obj_str = obj_str[:-1]
                if obj_str:
                    yield json.loads(obj_str)
                buffer = ''

def process_json(input_path, output_path=None, summary=False, no_output=False, save_summary=False):
    counts = Counter()
    applies_to_counter = Counter()
    applies_to_per_type = defaultdict(list)

    # Prepare CSV writer if output is enabled
    csv_file = None
    writer = None
    if not no_output and output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        csv_file = open(output_path, 'w', newline='', encoding='utf-8')
        writer = csv.writer(csv_file)
        writer.writerow(['Name', 'Type', 'Applies To'])

    # Stream JSON and process row by row
    for item in stream_json_array(input_path):
        name = item.get('name', '')
        type_ = item.get('type', '')
        applies_to_list = item.get('applies_to', [])
        applies_to_str = ', '.join(applies_to_list)

        counts[type_] += 1
        for a in applies_to_list:
            applies_to_counter[a] += 1
        applies_to_per_type[type_].append(applies_to_list)

        # Write row immediately
        if writer:
            writer.writerow([name, type_, applies_to_str])

    # Close CSV file if open
    if csv_file:
        csv_file.close()
        print(f"CSV written to {output_path}")

    # Prepare summary data
    summary_data = {
        'types': {},
        'overall_applies_to_counts': dict(applies_to_counter)
    }

    for t, c in counts.items():
        target_lists = applies_to_per_type[t]
        unique_targets = sorted(set(a for sublist in target_lists for a in sublist))
        min_targets = min(len(sublist) for sublist in target_lists)
        max_targets = max(len(sublist) for sublist in target_lists)
        summary_data['types'][t] = {
            'count': c,
            'unique_applies_to': unique_targets,
            'min_targets_per_item': min_targets,
            'max_targets_per_item': max_targets
        }

    # Print summary if requested
    if summary:
        print("\nSummary:")
        for t, info in summary_data['types'].items():
            print(f"  {t}: {info['count']} items")
            print(f"    Unique applies_to: {info['unique_applies_to']}")
            print(f"    Min targets per item: {info['min_targets_per_item']}")
            print(f"    Max targets per item: {info['max_targets_per_item']}")
        print("\nOverall applies_to counts:")
        for a, c in summary_data['overall_applies_to_counts'].items():
            print(f"  {a}: {c}")

    # Save summary to JSON if requested
    if save_summary:
        summary_file = os.path.splitext(os.path.basename(input_path))[0] + '_summary.json'
        summary_path = os.path.join(os.path.dirname(output_path) if output_path else '.', summary_file)
        with open(summary_path, 'w', encoding='utf-8') as f:
            json.dump(summary_data, f, indent=2)
        print(f"Summary saved to {summary_path}")

def main():
    parser = argparse.ArgumentParser(description="Process a JSON file of item prefixes/suffixes to CSV.")
    parser.add_argument('--input', type=str, required=True, help='Input JSON file path')
    parser.add_argument('--output', type=str, default='output/output.csv', help='Output CSV file path')
    parser.add_argument('--summary', action='store_true', help='Print summary of items processed')
    parser.add_argument('--no-output', action='store_true', help='Do not write output CSV (for debugging)')
    parser.add_argument('--save-summary', action='store_true', help='Save summary to a JSON file')

    args = parser.parse_args()

    process_json(
        input_path=args.input,
        output_path=args.output,
        summary=args.summary,
        no_output=args.no_output,
        save_summary=args.save_summary
    )

if __name__ == "__main__":
    main()
