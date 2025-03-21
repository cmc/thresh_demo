from flask import Flask, request, jsonify
import os
import json
import base64
import random
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
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
devices = {}  # {device_id: {"public_key": key, "rsa_key": key}}

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
    
    # Load public keys
    public_key = serialization.load_pem_public_key(
        data['public_key'].encode()
    )
    rsa_key = serialization.load_pem_public_key(
        data['rsa_key'].encode()
    )
    
    # Store device info in both places
    devices[device_id] = {
        "public_key": public_key,
        "rsa_key": rsa_key
    }
    
    # Also store in enrolled_devices for compatibility
    enrolled_devices[device_id] = {
        "public_key": data['public_key'],  # Store PEM format
        "rsa_key": data['rsa_key']
    }
    
    print(f"✓ Device {device_id} enrolled")
    print(f"  Public key: {data['public_key']}")
    print(f"  RSA key: {data['rsa_key']}")
    print(f"  Total devices enrolled: {len(enrolled_devices)}")
    
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

if __name__ == '__main__':
    app.run(debug=True, port=5010)
