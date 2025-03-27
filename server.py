from flask import Flask, request, jsonify
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
import base64
import json
import random
from eth_account import Account
from eth_account._utils.structured_data.hashing import hash_message
from eth_hash.auto import keccak

app = Flask(__name__)

# Configuration
ENROLLMENT_PASSWORD = "supersecurepassword"
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

@app.route('/enroll', methods=['POST'])
def enroll():
    data = request.json
    device_id = data['device_id']
    
    # Load public key
    public_key = serialization.load_pem_public_key(
        data['public_key'].encode()
    )
    
    # Store device info
    devices[device_id] = {
        "public_key": public_key
    }
    
    print(f"✓ Device {device_id} enrolled")
    print(f"  Public key: {data['public_key']}")
    print(f"  Total devices enrolled: {len(devices)}")
    
    return jsonify({"status": "success", "message": f"Device {device_id} enrolled"})

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
    """Initialize a new DKG round"""
    global dkg_round
    dkg_round = 1
    dkg_shares.clear()
    print("\n=== Starting New DKG Round ===")
    return jsonify({"status": "success", "round": dkg_round})

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
    """Initialize a new signing round"""
    data = request.json
    message_hash = data['message_hash']
    
    # Reset signing data
    signing_data.clear()
    signing_data.update({
        "commitments": {},
        "mta_values": {},
        "sig_shares": {},
        "R": None,
        "message_hash": message_hash
    })
    
    print("\n=== Starting New Signing Round ===")
    print(f"  Message hash: {message_hash}")
    return jsonify({"status": "success", "message_hash": message_hash})

@app.route('/signing/commit', methods=['POST'])
def submit_commitment():
    """Submit R_i and Gamma_i commitments"""
    data = request.json
    device_id = data['device_id']
    commitment = data['commitment']
    
    print(f"\n=== Received Commitment from {device_id} ===")
    print(f"  R_i: ({commitment['R_i']['x']}, {commitment['R_i']['y']})")
    print(f"  Gamma_i: ({commitment['Gamma_i']['x']}, {commitment['Gamma_i']['y']})")
    
    signing_data["commitments"][device_id] = commitment
    
    if len(signing_data["commitments"]) == TOTAL_SIGNERS:
        print("  ✓ All commitments received")
        return jsonify({
            "status": "complete",
            "commitments": signing_data["commitments"]
        })
    
    print(f"  → Waiting for more commitments ({len(signing_data['commitments'])}/{TOTAL_SIGNERS})")
    return jsonify({
        "status": "waiting",
        "current": len(signing_data["commitments"]),
        "total": TOTAL_SIGNERS
    })

@app.route('/signing/mta', methods=['POST'])
def submit_mta():
    """Submit MtA protocol values"""
    data = request.json
    from_device = data['from']
    to_device = data['to']
    delta = data['delta']
    
    print(f"\n=== Received MtA Value ===")
    print(f"  From: {from_device}")
    print(f"  To: {to_device}")
    
    if from_device not in signing_data["mta_values"]:
        signing_data["mta_values"][from_device] = {}
    signing_data["mta_values"][from_device][to_device] = delta
    
    # Count total MtA values
    total_values = sum(len(values) for values in signing_data["mta_values"].values())
    expected_values = TOTAL_SIGNERS * (TOTAL_SIGNERS - 1)  # Each device sends to all others
    
    if total_values == expected_values:
        print("  ✓ All MtA values received")
        return jsonify({
            "status": "complete",
            "mta_values": signing_data["mta_values"]
        })
    
    print(f"  → Waiting for more MtA values ({total_values}/{expected_values})")
    return jsonify({
        "status": "waiting",
        "current": total_values,
        "total": expected_values
    })

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
    app.run(debug=True, port=5010)
