import json

# Define the input file path
file_path = 'backend/stores/fixtures/stores_data.json'

# Non-nullable fields in the Store model (based on current models.py and Django defaults)
NON_NULLABLE_STORE_FIELDS = {
    'name',
    'address',
    'avg_rating', # Has a default, but the field itself is non-nullable for direct assignment
}

problematic_entries = []

try:
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for entry in data:
        if entry.get('model') == 'stores.store':
            pk = entry.get('pk')
            fields = entry.get('fields', {})
            
            for field_name, value in fields.items():
                if value is None and field_name in NON_NULLABLE_STORE_FIELDS:
                    problematic_entries.append(
                        f"Store (pk={pk}) has null value for non-nullable field: '{field_name}'"
                    )

    if problematic_entries:
        print("Found issues in stores_data.json:")
        for issue in problematic_entries:
            print(f"- {issue}")
    else:
        print("No null values found in non-nullable Store fields in stores_data.json.")

except FileNotFoundError:
    print(f"Error: File not found at {file_path}")
except json.JSONDecodeError as e:
    print(f"Error decoding JSON from {file_path}: {e}")
except Exception as e:
    print(f"An unexpected error occurred: {e}")
