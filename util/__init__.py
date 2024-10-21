import gzip
import io
import json
import os
from dotenv import load_dotenv


def read_env():
    load_dotenv()
    return {
        'retina_display': True if os.getenv('RETINA_DISPLAY', 'false').lower().startswith('t') else False,
        'people_to_generate': int(os.getenv('PEOPLE_TO_GENERATE', 100)),
        'sleep_for_addresses': int(os.getenv('SLEEP_FOR_ADDRESSES', 3)),
        'use_proxy': True if os.getenv('USE_PROXY', 'false').lower().startswith('t') else False,
        'proxy_auth': True if os.getenv('PROXY_AUTH', 'false').lower().startswith('t') else False,
        'proxy_host': os.getenv('PROXY_HOST', ''),
        'proxy_port': os.getenv('PROXY_PORT', ''),
        'proxy_user': os.getenv('PROXY_USER', ''),
        'proxy_pass': os.getenv('PROXY_PASS', ''),
        'proxy_type': os.getenv('PROXY_TYPE', 'http').strip().lower(),
        'enable_failsafe': True if os.getenv('ENABLE_FAILSAFE', 'true').lower().startswith('t') else False,
    }


def decompress_if_gzip(blob):
    # Check if the blob starts with the Gzip signature
    if blob.startswith(b'\x1f\x8b'):
        try:
            # Decompress the blob using Gzip
            with gzip.GzipFile(fileobj=io.BytesIO(blob)) as f:
                decompressed_data = f.read()
                return decompressed_data
        except Exception as e:
            # Handle decompression errors
            print(f"Error decompressing data: {e}")
            return None
    else:
        # Return the original data if it's not Gzip-compressed
        return blob


def decode_and_parse_json(binary_data):
    try:
        # Try to decode the binary data to a UTF-8 string
        decoded_data = binary_data.decode('utf-8')

        # Check if the decoded string starts with '{' or '[' (typical for JSON objects or arrays)
        if decoded_data.startswith('{') or decoded_data.startswith('['):
            # Try to parse the decoded string as JSON
            parsed_json = json.loads(decoded_data)
            return parsed_json
        else:
            print("Data does not appear to be JSON.")
            return None
    except (UnicodeDecodeError, json.JSONDecodeError) as e:
        # Handle decoding or JSON parsing errors
        print(f"Error decoding or parsing JSON: {e}")
        return None
