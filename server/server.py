from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import base64
import json
import random
from eth_account import Account
from eth_account._utils.structured_data.hashing import hash_message
from eth_hash.auto import keccak
from flask_cors import CORS
import secrets
from eth_utils import to_bytes, to_hex, decode_hex, encode_hex
import sys
import logging
from eth_account import Account
from eth_account._utils.legacy_transactions import (
    serializable_unsigned_transaction_from_dict,
    encode_transaction
)
from termcolor import colored

# Load config first
with open('config.json', 'r') as f:
    SERVER_CONFIG = json.load(f)

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Ensure Flask's logger also uses DEBUG level
app.logger.setLevel(logging.DEBUG)
for handler in app.logger.handlers:
    handler.setLevel(logging.DEBUG)

# Configuration
transactions = []  # Store pending transactions
partial_signatures = {}
backup_ciphertext = None  # Store encrypted key

# Store enrolled devices & their public keys
enrolled_devices = {}  
commitments = {}  
shares = {}  
private_shares = {}  # device_id -> ki
public_shares = {}  # device_id -> Ki

# Threshold settings
threshold = 3
total_signers = 5

# Store device information
devices = {}  # {device_id: {"public_key": key}}

# Constants
THRESHOLD = 3
TOTAL_SIGNERS = 5
CURVE = ec.SECP256K1()
# SECP256K1 curve order (n)
CURVE_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141

# Storage
dkg_shares = {}  # {device_id: {"commitments": [], "shares": {}}}
dkg_round = 0
signing_data = {
    "commitments": {},  # {device_id: {"R_i": point, "Gamma_i": point}}
    "mta_values": {},  # {from_device: {to_device: delta_ij}}
    "sig_shares": {},  # {device_id: sigma_i}
    "R": None,  # Combined R value
    "message_hash": None
}

# Global state
dkg_state = None
signing_state = None

# Test EOAs that we want to generate signatures for
TEST_EOAS = [
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44f"
]

# Test EOAs and their transactions
TEST_TRANSACTIONS = {
    "0x742d35Cc6634C0532925a3b844Bc454e4438f44e": {
        "to": decode_hex("0x742d35Cc6634C0532925a3b844Bc454e4438f44f"),  # Convert to bytes
        "value": 1000000000000000000,  # 1 ETH in wei (as int)
        "nonce": 0,  # as int
        "gasPrice": 20000000000,  # 20 Gwei (as int)
        "gas": 21000,  # as int
        "chainId": 1,  # Mainnet
        "data": b''  # as bytes
    }
}

def format_tx_for_json(tx):
    """Convert transaction values to hex strings for JSON"""
    return {
        "to": to_hex(tx["to"]),
        "value": hex(tx["value"]),
        "nonce": hex(tx["nonce"]),
        "gasPrice": hex(tx["gasPrice"]),
        "gas": hex(tx["gas"]),
        "chainId": tx["chainId"],
        "data": to_hex(tx["data"])
    }

# Utility: Hash Ethereum transactions
def hash_transaction(tx_data):
    tx_json = json.dumps(tx_data, sort_keys=True).encode()
    return keccak(tx_json)

# Utility: Verify request signature
def verify_signature(device_id, request_data, signature):
    """Verify that the request was signed with the iPhone's private key"""
    if device_id not in enrolled_devices:
        return False

    public_key_pem = enrolled_devices[device_id]["public_key"]
    try:
        # Debug logging to see what we're receiving
        print(f"Received PEM: {public_key_pem}")
        
        # Ensure PEM is properly formatted and encoded
        if not public_key_pem.startswith('-----BEGIN PUBLIC KEY-----'):
            return False
            
        public_key = serialization.load_pem_public_key(public_key_pem.encode())
        public_key.verify(
            base64.b64decode(signature),
            request_data.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        return True
    except Exception as e:
        print(f"Signature verification failed: {e}")
        return False

# Utility: Generate an Ethereum key pair
def generate_key_pair():
    private_key = ec.generate_private_key(ec.SECP256K1())
    public_key = private_key.public_key()
    return private_key, public_key

# Utility: Convert a public key to Ethereum address
def public_key_to_eth_address(public_key):
    pub_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )[1:]  # Drop the first byte (format indicator)

    address = keccak(pub_bytes)[-20:]  # Ethereum address = last 20 bytes of Keccak-256
    return f"0x{address.hex()}"

@app.route('/device/enroll', methods=['POST'])
def enroll_device():
    data = request.json
    if not data or 'device_id' not in data or 'enrollment_key' not in data:
        return jsonify({'error': 'Missing device_id or enrollment_key'}), 400
        
    # Check enrollment key against config
    if data['enrollment_key'] != SERVER_CONFIG['enrollment_key']:
        return jsonify({'error': 'Invalid enrollment key'}), 401
        
    device_id = data['device_id']
    
    # Check if we've hit max devices
    if len(SERVER_CONFIG['allowed_devices']) >= SERVER_CONFIG['max_devices']:
        return jsonify({'error': 'Maximum number of devices reached'}), 400
        
    # Add device if not already enrolled
    if device_id not in SERVER_CONFIG['allowed_devices']:
        SERVER_CONFIG['allowed_devices'].append(device_id)
        with open('config.json', 'w') as f:
            json.dump(SERVER_CONFIG, f, indent=2)
            
    return jsonify({'status': 'ok', 'device_id': device_id})

@app.route('/distribute_shares', methods=['POST'])
def distribute_shares():
    data = request.json
    device_id = data['device_id']
    encrypted_shares = data['encrypted_shares']
    
    print(f"\n=== Receiving shares from {device_id} ===")
    print(f"Number of encrypted shares: {len(encrypted_shares)}")
    
    # Store the encrypted shares
    if device_id not in shares:
        shares[device_id] = {}
    shares[device_id]['encrypted_shares'] = encrypted_shares
    
    # Log share details
    for receiver_id, share_data in encrypted_shares.items():
        print(f"  Share for {receiver_id}:")
        print(f"    Encrypted share size: {len(share_data['encrypted_share'])} bytes")
        print(f"    Encrypted key size: {len(share_data['encrypted_key'])} bytes")
        print(f"    IV size: {len(share_data['iv'])} bytes")
    
    return jsonify({
        "status": "success",
        "message": f"Shares from {device_id} stored",
        "shares_count": len(encrypted_shares)
    })

@app.route('/generate_public_key', methods=['GET'])
def generate_public_key():
    if len(devices) < total_signers:
        return jsonify({"error": "Not enough enrolled devices"}), 400
        
    # For now, just return the first device's public key
    # This will be updated with proper key aggregation
    first_device = list(devices.values())[0]
    eth_address = public_key_to_eth_address(first_device["public_key"])
    
    return jsonify({
        "ethereum_address": eth_address,
        "enrolled_devices": len(devices)
    })

@app.route('/request_txn_signature', methods=['POST'])
def request_txn_signature():
    """Request threshold signing from iPhones."""
    data = request.json
    transaction_data = data.get("transaction")

    if not transaction_data:
        return jsonify({"error": "No transaction data provided"}), 400

    txn_hash = hash_transaction(transaction_data).hex()
    transactions.append({"txn_hash": txn_hash, "transaction_data": transaction_data})

    return jsonify({"message": "Transaction signature requested", "txn_hash": txn_hash})

@app.route('/submit_partial_signature', methods=['POST'])
def submit_partial_signature():
    """iPhones return partial signatures for aggregation."""
    data = request.json
    device_id = data.get("device_id")
    partial_sig = data.get("partial_signature")
    signature = data.get("signature")

    print(f"\nReceived partial signature from {device_id}")
    print(f"  Signature length: {len(partial_sig) if partial_sig else 'None'}")

    if device_id not in enrolled_devices:
        print(f"  ✗ Device {device_id} not enrolled")
        print(f"  Currently enrolled devices: {list(enrolled_devices.keys())}")
        return jsonify({"error": "Device not enrolled"}), 403

    # Store the partial signature
    partial_signatures[device_id] = partial_sig
    print(f"  ✓ Partial signature stored")
    print(f"  Total signatures collected: {len(partial_signatures)}/{threshold}")

    if len(partial_signatures) >= threshold:
        print("\nThreshold reached! Aggregating signatures...")
        # For now, just concatenate the signatures
        final_signature = "".join(list(partial_signatures.values())[:threshold])
        print(f"  Final signature length: {len(final_signature)}")
        return jsonify({
            "final_signature": final_signature, 
            "signature_ready": True
        })

    return jsonify({
        "message": "Partial signature accepted, waiting for more",
        "current_count": len(partial_signatures),
        "threshold": threshold
    }), 202

@app.route('/recover_private_key', methods=['POST'])
def recover_private_key():
    """Recovers the private key using threshold decryption (requires t trusted parties)."""
    data = request.json
    recovery_shares = data.get("recovery_shares")
    signature = data.get("signature")

    if not verify_signature("admin", json.dumps({"recovery_shares": recovery_shares}), signature):
        return jsonify({"error": "Invalid signature"}), 403

    if len(recovery_shares) < threshold:
        return jsonify({"error": "Not enough shares to recover the private key."}), 403

    return jsonify({"recovered_private_key": "Decryption successful (mock response)"})

@app.route('/dkg/start', methods=['POST'])
def start_dkg():
    global dkg_state
    target_eoa = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
    raw_tx = TEST_TRANSACTIONS[target_eoa]
    display_tx = format_tx_for_json(raw_tx)
    
    dkg_state = {
        'status': 'in_progress',
        'commitments': {},
        'shares': {},
        'target_eoa': target_eoa,
        'transaction': raw_tx,  # Store raw transaction
        'display_transaction': display_tx  # Store display version
    }
    
    return jsonify({
        'status': 'ok', 
        'target_eoa': target_eoa,
        'transaction': display_tx
    })

@app.route('/dkg/submit', methods=['POST'])
def submit_dkg_data():
    """Submit DKG shares and commitments"""
    data = request.json
    device_id = data['device_id']
    commitments = data['commitments']
    shares = data['shares']
    
    print(f"\n=== Received DKG Data from {device_id} ===")
    print(f"  Commitments: {len(commitments)}")
    print(f"  Shares: {len(shares)}")
    
    # Store the data
    dkg_shares[device_id] = {
        "commitments": commitments,
        "shares": shares
    }
    
    # Check if we have all shares
    if len(dkg_shares) == TOTAL_SIGNERS:
        print("  ✓ All DKG shares received")
        return jsonify({
            "status": "complete",
            "shares": dkg_shares
        })
    
    print(f"  → Waiting for more shares ({len(dkg_shares)}/{TOTAL_SIGNERS})")
    return jsonify({
        "status": "waiting",
        "current": len(dkg_shares),
        "total": TOTAL_SIGNERS
    })

@app.route('/signing/start', methods=['POST'])
def start_signing():
    global signing_state
    if not dkg_state:
        return jsonify({'error': 'DKG not initialized'}), 400
    
    target_eoa = dkg_state['target_eoa']
    display_tx = dkg_state['display_transaction']  # Use display version
    message_hash = "0x" + secrets.token_hex(32)
    
    signing_state = {
        'status': 'in_progress',
        'target_eoa': target_eoa,
        'message_hash': message_hash,
        'transaction': dkg_state['transaction'],  # Store raw version
        'display_transaction': display_tx,  # Store display version
        'commitments': {},
        'mta_values': {}
    }
    
    return jsonify({
        'status': 'ok',
        'target_eoa': target_eoa,
        'message_hash': message_hash,
        'transaction': display_tx  # Send display version
    })

@app.route('/signing/commit', methods=['POST'])
def submit_signing_commitment():
    if not signing_state:
        return jsonify({'error': 'Signing not initialized'}), 400
    
    data = request.json
    device_id = data['device_id']
    commitment = data['commitment']
    
    logger.debug(f"Received commitment from {device_id}")
    
    signing_state['commitments'][device_id] = {
        'k_i': commitment['k_i'],
        'gamma_i': commitment['gamma_i'],
        'R_i': commitment['R_i']
    }
    
    # If we have all commitments, generate final signature
    if len(signing_state['commitments']) == len(dkg_state['shares']):
        logger.debug("All commitments received, generating final signature...")
        
        # Combine shares to generate final signature
        k = 0
        gamma = 0
        for device_data in signing_state['commitments'].values():
            k = (k + int(device_data['k_i'], 16)) % CURVE_ORDER
            gamma = (gamma + int(device_data['gamma_i'], 16)) % CURVE_ORDER
        
        # Calculate R = k * G
        R = ec.derive_private_key(k, CURVE).public_key()
        r = R.public_numbers().x % CURVE_ORDER
        
        # Calculate s using combined shares
        message_int = int(signing_state['message_hash'], 16)
        k_inv = pow(k, -1, CURVE_ORDER)
        s = (k_inv * (message_int + r * gamma)) % CURVE_ORDER
        
        # Calculate v (27 or 28 depending on y coordinate)
        v = 27 + (R.public_numbers().y % 2)
        
        # Create final signed transaction
        signed_tx = {
            **signing_state['transaction'],
            "r": hex(r),
            "s": hex(s),
            "v": hex(v)
        }
        
        # Create serialized transaction
        tx_unsigned = serializable_unsigned_transaction_from_dict(signing_state['transaction'])
        tx_signed = encode_transaction(tx_unsigned, vrs=(v, r, s))
        
        # Store in signing state
        signing_state['final_signature'] = {
            'r': hex(r),
            's': hex(s),
            'v': hex(v)
        }
        signing_state['signed_transaction'] = signed_tx
        signing_state['serialized_transaction'] = encode_hex(tx_signed)
        signing_state['status'] = 'completed'
        
        # Print final transaction details in green
        logger.info("\n" + colored("=== 🔐 Final Signed Transaction ===", 'green', attrs=['bold']))
        logger.info(colored("\nTransaction Details:", 'green'))
        logger.info(colored(json.dumps(signed_tx, indent=2), 'green'))
        
        logger.info(colored("\nSignature Components:", 'green'))
        logger.info(colored(f"R: {hex(r)}", 'green'))
        logger.info(colored(f"S: {hex(s)}", 'green'))
        logger.info(colored(f"V: {hex(v)}", 'green'))
        
        logger.info(colored("\nBroadcastable Transaction:", 'green'))
        logger.info(colored(f"Hex: {encode_hex(tx_signed)}", 'green'))
        
        logger.info(colored("\nParticipant Information:", 'green'))
        logger.info(colored(f"Total Participants: {len(signing_state['commitments'])}", 'green'))
        for participant_id in signing_state['commitments']:
            logger.info(colored(f"• {participant_id} contributed partial signature", 'green'))
        
        return jsonify({'status': 'completed'})
    
    return jsonify({'status': 'ok'})

@app.route('/signing/mta', methods=['POST'])
def submit_mta():
    if not signing_state:
        return jsonify({'error': 'Signing not initialized'}), 400
    
    data = request.json
    from_device = data['from']
    to_device = data['to']
    delta = data['delta']
    
    logger.info(f"\n=== Received MtA Value ===")
    logger.info(f"  From: {from_device}")
    logger.info(f"  To: {to_device}")
    
    # Store MtA value
    if 'mta_values' not in signing_state:
        signing_state['mta_values'] = {}
    
    mta_key = f"{from_device}->{to_device}"
    signing_state['mta_values'][mta_key] = delta
    
    # Calculate n from number of unique devices in commitments
    n = len(signing_state['commitments'])
    expected_mta_count = n * (n - 1)  # Each device sends to every other device
    current_count = len(signing_state['mta_values'])
    
    logger.info(f"  MtA Progress: {current_count}/{expected_mta_count}")
    logger.info(f"  Number of participants: {n}")
    
    # Only proceed when we have all MtA values and haven't generated signature yet
    if current_count < expected_mta_count or signing_state.get('status') == 'completed':
        return jsonify({'status': 'ok'})
    
    # Now we really have all MtA values and haven't generated signature yet
    logger.info(colored("\n✓ All MtA values received!", 'green'))
    
    # Generate final signature
    k = 0
    gamma = 0
    for device_data in signing_state['commitments'].values():
        k = (k + int(device_data['k_i'], 16)) % CURVE_ORDER
        gamma = (gamma + int(device_data['gamma_i'], 16)) % CURVE_ORDER
    
    # Calculate R = k * G
    R = ec.derive_private_key(k, CURVE).public_key()
    r = R.public_numbers().x % CURVE_ORDER
    
    # Calculate s using combined shares
    message_int = int(signing_state['message_hash'], 16)
    k_inv = pow(k, -1, CURVE_ORDER)
    s = (k_inv * (message_int + r * gamma)) % CURVE_ORDER
    
    # Calculate v (27 or 28 depending on y coordinate)
    v = 27 + (R.public_numbers().y % 2)
    
    # Create final signed transaction with hex strings
    raw_tx = signing_state['transaction']
    signed_tx = {
        "to": to_hex(raw_tx["to"]),
        "value": hex(raw_tx["value"]),
        "nonce": hex(raw_tx["nonce"]),
        "gasPrice": hex(raw_tx["gasPrice"]),
        "gas": hex(raw_tx["gas"]),
        "chainId": raw_tx["chainId"],
        "data": to_hex(raw_tx["data"]),
        "r": hex(r),
        "s": hex(s),
        "v": hex(v)
    }
    
    # Create serialized transaction
    tx_unsigned = serializable_unsigned_transaction_from_dict(signing_state['transaction'])
    tx_signed = encode_transaction(tx_unsigned, vrs=(v, r, s))
    
    # Store in signing state
    signing_state['final_signature'] = {
        'r': hex(r),
        's': hex(s),
        'v': hex(v)
    }
    signing_state['signed_transaction'] = signed_tx
    signing_state['serialized_transaction'] = encode_hex(tx_signed)
    signing_state['status'] = 'completed'
    
    # Print final transaction in green
    logger.info(colored("\n=== 🔐 Final Signed Transaction ===", 'green', attrs=['bold']))
    logger.info(colored("\nTransaction Details:", 'green'))
    logger.info(colored(json.dumps(signed_tx, indent=2), 'green'))
    
    logger.info(colored("\nSignature Components:", 'green'))
    logger.info(colored(f"R: {hex(r)}", 'green'))
    logger.info(colored(f"S: {hex(s)}", 'green'))
    logger.info(colored(f"V: {hex(v)}", 'green'))
    
    logger.info(colored("\nBroadcastable Transaction:", 'green'))
    logger.info(colored(f"Hex: {encode_hex(tx_signed)}", 'green'))
    
    logger.info(colored("\nParticipant Information:", 'green'))
    logger.info(colored(f"Total Participants: {len(signing_state['commitments'])}", 'green'))
    for participant_id in signing_state['commitments']:
        logger.info(colored(f"• {participant_id} contributed partial signature", 'green'))
    
    return jsonify({'status': 'completed'})

@app.route('/signing/share', methods=['POST'])
def submit_signature_share():
    """Submit partial signature share"""
    data = request.json
    device_id = data['device_id']
    share = data['share']
    
    print(f"\n=== Received Signature Share from {device_id} ===")
    signing_data["sig_shares"][device_id] = share
    
    if len(signing_data["sig_shares"]) == THRESHOLD:
        print("  ✓ Threshold of signature shares received")
        # Combine shares into final signature
        shares = list(signing_data["sig_shares"].values())
        R = signing_data["R"]
        
        # Get r value from R point
        r = int(R.public_numbers().x) % CURVE_ORDER
        
        # Sum all shares modulo curve order
        s = sum(int(share, 16) for share in shares) % CURVE_ORDER
        
        # Standard v value for Ethereum
        v = 27
        
        final_signature = {
            'r': hex(r),
            's': hex(s),
            'v': hex(v)
        }
        
        print("\n=== Final Signature ===")
        print(f"  R: {final_signature['r']}")
        print(f"  S: {final_signature['s']}")
        print(f"  V: {final_signature['v']}")
        
        return jsonify({
            "status": "complete",
            "signature": final_signature
        })
    
    print(f"  → Waiting for more shares ({len(signing_data['sig_shares'])}/{THRESHOLD})")
    return jsonify({
        "status": "waiting",
        "current": len(signing_data["sig_shares"]),
        "total": THRESHOLD
    })

if __name__ == '__main__':
    app.run(host=SERVER_CONFIG['host'], port=SERVER_CONFIG['port'], debug=True)
