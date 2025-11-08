import os
import json
import argparse
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_DIR, 'data', 'college_info.json')


def main():
    parser = argparse.ArgumentParser(description='Admin update for college data JSON')
    parser.add_argument('source', help='Path to JSON file to import (will merge keys)')
    parser.add_argument('--token', required=True, help='Admin token (must match ADMIN_TOKEN env)')
    args = parser.parse_args()

    admin_token = os.environ.get('ADMIN_TOKEN')
    if not admin_token:
        print('ADMIN_TOKEN not set in environment. Set it in .env or as an environment variable.')
        return
    if args.token != admin_token:
        print('Invalid admin token. Aborting.')
        return

    try:
        with open(args.source, 'r', encoding='utf-8') as f:
            new_data = json.load(f)
    except Exception as e:
        print('Failed to read source JSON:', e)
        return

    try:
        with open(DATA_PATH, 'r', encoding='utf-8') as f:
            base = json.load(f)
    except FileNotFoundError:
        base = {}

    # merge: for simple lists/objects we replace or extend sensibly
    for k, v in new_data.items():
        if isinstance(v, list):
            base.setdefault(k, [])
            # naive merge: append items that don't have identical 'id'
            existing_ids = {item.get('id') for item in base[k] if isinstance(item, dict) and 'id' in item}
            for item in v:
                if isinstance(item, dict) and item.get('id') in existing_ids:
                    # replace existing by id
                    base[k] = [item if (isinstance(it, dict) and it.get('id')==item.get('id')) else it for it in base[k]]
                else:
                    base[k].append(item)
        elif isinstance(v, dict):
            base.setdefault(k, {})
            base[k].update(v)
        else:
            base[k] = v

    try:
        with open(DATA_PATH, 'w', encoding='utf-8') as f:
            json.dump(base, f, ensure_ascii=False, indent=2)
        print('Data updated successfully.')
    except Exception as e:
        print('Failed to write data file:', e)


if __name__ == '__main__':
    main()
