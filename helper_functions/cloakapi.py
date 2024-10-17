import hashlib
import hmac
import json
import urllib.parse
import requests
import datetime
from dotenv import load_dotenv
import os

load_dotenv('.env')

private_key = os.getenv('cloak_private_key')
public_key = os.getenv('cloak_public_key')

# Generate Signature
def generate_signature(http_method, path, query_params, headers, payload, private_key, service):
    # Ensure query_params is a dictionary
    query_params = query_params if query_params else {}

    # Step 1: Create the canonical request
    canonical_uri = urllib.parse.quote(path, safe='/')
    canonical_querystring = '&'.join(
        f"{urllib.parse.quote(k, safe='')}={urllib.parse.quote(v, safe='')}"
        for k, v in sorted(query_params.items())
    )
    signed_headers = sorted(headers.keys())
    canonical_headers = ''.join(
        f"{k.lower()}:{v.strip()}\n" for k, v in sorted(headers.items())
    )
    signed_headers_string = ';'.join(k.lower() for k in signed_headers)

    if isinstance(payload, dict):
        payload_str = json.dumps(payload, sort_keys=True)  # Ensure consistent key order
        payload_bytes = payload_str.encode('utf-8')
        payload_hash = hashlib.sha256(payload_bytes).hexdigest()
    else:
        payload_hash = hashlib.sha256(payload).hexdigest()


    canonical_request = (
        f"{http_method}\n"
        f"{canonical_uri}\n"
        f"{canonical_querystring}\n"
        f"{canonical_headers}\n"
        f"{signed_headers_string}\n"
        f"{payload_hash}"
    )
    # Step 2: Create the string to sign
    algorithm = "CLOAK-AUTH"
    formatted_date = datetime.date.today().strftime('%Y%m%d') + 'T000000Z'
    date_stamp = formatted_date[:8]

    string_to_sign = (
        f"{algorithm}\n"
        f"{formatted_date}\n"
        f"{hashlib.sha256(canonical_request.encode('utf-8')).hexdigest()}"
    )
    # Step 3: Calculate the signing key
    def sign(key, msg):
        return hmac.new(key, msg.encode('utf-8'), hashlib.sha256).digest()

    date_key = sign(("CLOAK-AUTH" + private_key).encode('utf-8'), date_stamp)
    date_service_key = sign(date_key, service)
    signing_key = sign(date_service_key, "cloak_request")


    # Step 4: Calculate the signature
    signature = hmac.new(signing_key, string_to_sign.encode('utf-8'), hashlib.sha256).hexdigest()

    return signature

# Extract URL Information

def extract_url_info(url):
    parsed_url = urllib.parse.urlparse(url)
    path = parsed_url.path
    query_params = urllib.parse.parse_qs(parsed_url.query)
    # Convert query_params values from list to single value
    query_params = {k: v[0] for k, v in query_params.items()}
    return path, query_params

def check_connection():
    # Get all policies (GET Example)

    url = 'https://ext-api.cloak.gov.sg/prod/L4/tabular/policies?'
    http_method = "GET"
    signed_headers = {
        "Content-Type": "application/json"
    }
    path, query_params = extract_url_info(url)
    service = "tda"
    payload = b''

    signature = generate_signature(http_method, path, query_params, signed_headers, payload, private_key, service)
    authorization = f'CLOAK-AUTH Credential={public_key},SignedHeaders=content-type,Signature={signature}'
    headers = {'Content-Type':'application/json', 'Accept':'application/json', 'Authorization': f'{authorization}', 'x-cloak-service': f'{service}'}
    response = requests.get(url, headers=headers, verify=False)
    return response

def cloak_transform(record):
    # Transform Endpoint
    http_method = "POST"
    url = 'https://ext-api.cloak.gov.sg/prod/L4/transform'
    payload = {
        "text": f"{record}",
        "language": "en",
        "entities": [
            "PERSON",
            "SG_NRIC_FIN",
            "SG_BANK_ACCOUNT_NUMBER",
            "SG_ADDRESS",
            "PHONE_NUMBER",
            "EMAIL_ADDRESS"
        ],
        "score_threshold": 0.3,
        "anonymizers": {
            "SG_NRIC_FIN": {
                "type": "replace",
                "new_value": "<SG_NRIC_FIN>"
            },
            "PHONE_NUMBER": {
                "type": "mask",
                "masking_char": "*",
                "chars_to_mask": 4,
                "from_end": False
            },
            "PERSON": {
                "type": "replace",
                "new_value": "<NAME>"
            },
            "EMAIL_ADDRESS": {
                "type": "encrypt",
                "key": "12345678901234567890123456789012"
            },
            "SG_ADDRESS": {
                "type": "replace",
                "new_value": "<SG_ADDRESS>"
            },
            "SG_BANK_ACCOUNT_NUMBER": {
                "type": "replace",
                "new_value": "<SG_BANK_ACCOUNT_NUMBER>"
            }
        }
    }
    service = "fta"
    signed_headers = {
        "Content-Type": "application/json"
    }
    path, query_params = extract_url_info(url)
    signature = generate_signature(http_method, path, query_params, signed_headers, payload, private_key, service)
    authorization = f'CLOAK-AUTH Credential={public_key},SignedHeaders=content-type,Signature={signature}'
    headers = {'Content-Type':'application/json', 'Accept':'application/json', 'Authorization': f'{authorization}', 'x-cloak-service': f'{service}'}
    response = requests.post(url, headers=headers, json=payload, verify=False)
    response_dict = response.json()
    return response_dict["text"]


