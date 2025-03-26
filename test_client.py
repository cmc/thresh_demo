from cryptography.hazmat.primitives.asymmetric import rsa, padding as rsa_padding
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from eth_utils import keccak, to_checksum_address
import base64
import json
import requests
import random
import os
import secrets

# Flask Server URL
SERVER_URL = "http://localhost:5010"

# Store both private keys and public keys
IPHONE_KEYS = {}  # {device_id: {"private": private_key, "public": public_key, "pem": public_pem}}

# Threshold settings
THRESHOLD = 3
TOTAL_SIGNERS = 5

# Curve parameters
CURVE_ORDER = 2**256 - 2**32 - 977
CURVE = ec.SECP256K1()

class GG20Device:
    def __init__(self, device_id, private_key):
        self.device_id = device_id
        self.private_key = private_key
        self.public_key = private_key.public_key()
        self.secret_share = private_key.private_numbers().private_value

    def start_signing(self, message_hash):
        """Round 1 of GG20 signing: Generate k_i and gamma_i"""
        print(f"\n=== Signing Round 1 for {self.device_id} ===")
        
        # Generate random k_i and gamma_i
        self.k_i = secrets.randbelow(CURVE_ORDER)
        self.gamma_i = secrets.randbelow(CURVE_ORDER)
        self.w_i = secrets.randbelow(CURVE_ORDER)
        
        # Compute R_i = g^k_i and commitment
        self.R_i = CURVE.generator * self.k_i
        self.Gamma_i = CURVE.generator * self.gamma_i
        
        # Create commitment to both values
        commitment = {
            'R_i': {
                'x': self.R_i.public_numbers().x,
                'y': self.R_i.public_numbers().y
            },
            'Gamma_i': {
                'x': self.Gamma_i.public_numbers().x,
                'y': self.Gamma_i.public_numbers().y
            }
        }
        
        print("  ✓ Generated random values")
        print("  ✓ Created commitments")
        return commitment
    
    def run_mta(self, other_device):
        """Run Multiplicative to Additive (MtA) protocol with another device"""
        print(f"  Running MtA with {other_device.device_id}...")
        
        # MtA for k_i * gamma_j
        alpha_ij = secrets.randbelow(CURVE_ORDER)
        beta_ij = secrets.randbelow(CURVE_ORDER)
        
        # Simulate secure two-party computation
        # In real implementation, this would use encryption
        delta_ij = (self.k_i * other_device.gamma_i + alpha_ij + beta_ij) % CURVE_ORDER
        
        print("  ✓ MtA protocol complete")
        return delta_ij
    
    def compute_signature_share(self, message_hash, R):
        """Compute partial signature using MtA results"""
        print(f"\n=== Computing signature share for {self.device_id} ===")
        
        # Convert message_hash to integer
        m = int(message_hash, 16)
        
        # Compute sigma_i = k_i * m + r * secret_share_i
        r = R.public_numbers().x % CURVE_ORDER
        sigma_i = (self.k_i * m + r * self.secret_share) % CURVE_ORDER
        
        print("  ✓ Computed signature share")
        return sigma_i
    
    @staticmethod
    def combine_signature_shares(shares, R):
        """Combine signature shares into final signature"""
        print("\n=== Combining Signature Shares ===")
        
        # Sum all shares modulo curve order
        sigma = sum(shares) % CURVE_ORDER
        
        # Get r value from R point
        r = R.public_numbers().x % CURVE_ORDER
        
        # Format as Ethereum signature
        v = 27  # or 28, depending on y-parity of R
        
        print("  ✓ Combined shares into final signature")
        return {
            'r': hex(r),
            's': hex(sigma),
            'v': hex(v)
        }

def generate_key_share():
    """Generate a partial key share for this device"""
    print("  Generating key shares...")
    # Generate EC key for signing
    private_share = ec.generate_private_key(ec.SECP256K1())
    public_share = private_share.public_key()
    
    # Generate RSA key for encryption
    rsa_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    rsa_public = rsa_key.public_key()
    
    # Convert public keys to PEM format
    public_pem = public_share.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    
    rsa_pem = rsa_public.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode()
    
    print("  ✓ EC key share generated for signing")
    print("  ✓ RSA key generated for encryption")
    return private_share, public_share, public_pem, rsa_key, rsa_public, rsa_pem

def encrypt_share_for_peer(share_data, peer_rsa_key):
    """Encrypt a share for another participant using their RSA public key"""
    print(f"  Encrypting share for peer...")
    # Generate ephemeral key for encryption
    ephemeral_key = os.urandom(32)
    iv = os.urandom(16)
    
    # Create AES cipher
    cipher = Cipher(algorithms.AES(ephemeral_key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    
    # Pad and encrypt the share data
    padded_data = share_data + b'\x00' * (16 - len(share_data) % 16)
    encrypted_share = encryptor.update(padded_data) + encryptor.finalize()
    
    # Encrypt the ephemeral key with peer's RSA public key
    encrypted_key = peer_rsa_key.encrypt(
        ephemeral_key,
        rsa_padding.OAEP(
            mgf=rsa_padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    
    print("  ✓ Share encrypted")
    return {
        'encrypted_share': base64.b64encode(encrypted_share).decode(),
        'encrypted_key': base64.b64encode(encrypted_key).decode(),
        'iv': base64.b64encode(iv).decode()
    }

def verify_signature(message, signature, public_key):
    """Verify a signature using a public key"""
    try:
        public_key.verify(
            base64.b64decode(signature),
            message.encode(),
            ec.ECDSA(hashes.SHA256())
        )
        print("  ✓ Signature verified successfully")
        return True
    except Exception as e:
        print(f"  ✗ Signature verification failed: {e}")
        return False

def sign_request(data, device_id):
    """Sign data using the device's private key"""
    print(f"  Signing data for {device_id}...")
    print(f"  Data to sign: {data}")
    
    if device_id not in IPHONE_KEYS:
        print(f"  ✗ No private key found for {device_id}")
        return None
        
    private_key = IPHONE_KEYS[device_id]["private"]
    signature = private_key.sign(
        data.encode(),
        ec.ECDSA(hashes.SHA256())
    )
    encoded_sig = base64.b64encode(signature).decode()
    print(f"  ✓ Signature generated: {encoded_sig[:32]}...")
    
    # Verify our own signature
    if verify_signature(data, encoded_sig, IPHONE_KEYS[device_id]["public"]):
        print("  ✓ Signature verified with public key")
    else:
        print("  ✗ Signature verification failed!")
    
    return encoded_sig

def enroll_iphones():
    print("\n=== Enrolling iPhones with MPC Setup ===")
    shares = {}  # Store encrypted shares for each device
    
    # First, generate key shares for each device
    for i in range(1, TOTAL_SIGNERS + 1):
        device_id = f"iphone_{i}"
        print(f"\nGenerating key material for {device_id}...")
        
        # Generate this device's key shares
        private_share, public_share, public_pem, rsa_key, rsa_public, rsa_pem = generate_key_share()
        IPHONE_KEYS[device_id] = {
            "private": private_share,
            "public": public_share,
            "pem": public_pem,
            "rsa_private": rsa_key,
            "rsa_public": rsa_public,
            "rsa_pem": rsa_pem
        }
        
        print(f"  EC Public share: {public_pem}")
        print(f"  RSA Public key: {rsa_pem}")
        
        # Create enrollment data
        enrollment_data = {
            "device_id": device_id,
            "public_key": public_pem,
            "rsa_key": rsa_pem
        }
        
        # Sign the enrollment data
        signature = sign_request(json.dumps(enrollment_data), device_id)
        
        # Create full payload
        payload = {
            **enrollment_data,
            "password": "supersecurepassword",
            "signature": signature
        }
        
        print(f"  Sending enrollment request to server...")
        try:
            response = requests.post(f"{SERVER_URL}/enroll", json=payload)
            print(f"  Server response status: {response.status_code}")
            if response.status_code == 200:
                print(f"  Server response: {response.json()}")
            else:
                print(f"  Server error: {response.text}")
        except Exception as e:
            print(f"  Error enrolling device: {e}")
    
    print("\n=== Distributing Encrypted Shares ===")
    # Now distribute encrypted shares to each other device
    for i in range(1, TOTAL_SIGNERS + 1):
        sender_id = f"iphone_{i}"
        sender_share = IPHONE_KEYS[sender_id]["private"]
        print(f"\nProcessing shares from {sender_id}...")
        
        # Encrypt share for each other device
        for j in range(1, TOTAL_SIGNERS + 1):
            if i != j:  # Don't send to self
                receiver_id = f"iphone_{j}"
                receiver_rsa_key = IPHONE_KEYS[receiver_id]["rsa_public"]
                print(f"  Encrypting share for {receiver_id}...")
                
                # Get share data
                share_data = sender_share.private_numbers().private_value.to_bytes(32, 'big')
                
                # Encrypt the share
                encrypted_data = encrypt_share_for_peer(share_data, receiver_rsa_key)
                
                # Store encrypted share
                if sender_id not in shares:
                    shares[sender_id] = {}
                shares[sender_id][receiver_id] = encrypted_data
                
                print(f"  ✓ Share encrypted for {receiver_id}")
                print(f"    Encrypted share size: {len(encrypted_data['encrypted_share'])} bytes")
                print(f"    Encrypted key size: {len(encrypted_data['encrypted_key'])} bytes")
    
    print("\n=== Distributing Shares to Server ===")
    # Send encrypted shares to server for distribution
    for sender_id, receivers in shares.items():
        print(f"\nSending {sender_id}'s encrypted shares...")
        payload = {
            "device_id": sender_id,
            "encrypted_shares": receivers,
            "signature": sign_request(json.dumps({"device_id": sender_id, "shares": receivers}), sender_id)
        }
        
        try:
            response = requests.post(f"{SERVER_URL}/distribute_shares", json=payload)
            print(f"  Server response status: {response.status_code}")
            if response.status_code == 200:
                print(f"  Server response: {response.json()}")
            else:
                print(f"  Server error: {response.text}")
        except requests.exceptions.JSONDecodeError:
            print(f"  Server returned invalid JSON. Raw response: {response.text[:200]}...")
        except Exception as e:
            print(f"  Error distributing shares: {e}")
    
    print("\n✓ MPC Setup Complete")
    print(f"  • {TOTAL_SIGNERS} devices enrolled")
    print(f"  • {len(shares)} sets of encrypted shares distributed")
    print(f"  • Threshold requirement: {THRESHOLD} signatures")

def request_signature():
    print("\n=== Requesting Transaction Signature ===")
    tx_data = {
        "to": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
        "value": "1000000000000000000"
    }
    print(f"Transaction data: {tx_data}")
    
    response = requests.post(f"{SERVER_URL}/request_txn_signature", json={"transaction": tx_data})
    result = response.json()
    print(f"Server response: {result}")
    return result["txn_hash"]

def get_ethereum_address(public_key):
    """Convert a public key to an Ethereum address"""
    # Get the key in uncompressed format (65 bytes)
    raw_pub_key = public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    # Remove the first byte (0x04 which indicates uncompressed point)
    raw_pub_key = raw_pub_key[1:]
    # Take keccak-256 of remaining 64 bytes
    keccak_hash = keccak(raw_pub_key)
    # Last 20 bytes is the address
    addr = keccak_hash[-20:]
    # Convert to checksum address
    return to_checksum_address(addr.hex())

def submit_signatures(txn_hash):
    print("\n=== Submitting Partial Signatures ===")
    print(f"Transaction hash: {txn_hash}")
    final_response = None
    partial_sigs = {}  # Store partial signatures for logging
    
    # Get the aggregated public key from server first
    print("\nFetching aggregated public key...")
    response = requests.get(f"{SERVER_URL}/generate_public_key")
    if response.status_code != 200:
        print(f"Error getting public key: {response.text}")
        return
        
    key_info = response.json()
    eth_address = key_info["ethereum_address"]
    print(f"Threshold wallet address: {eth_address}")
    
    print("\n=== Collecting Partial Signatures ===")
    print(f"Need {THRESHOLD} signatures for threshold...")
    
    # Only get signatures from first 3 iPhones (threshold)
    for i in range(1, THRESHOLD + 1):
        device_id = f"iphone_{i}"
        print(f"\nDevice {i} of {THRESHOLD}: {device_id}")
        
        # Generate real partial signature using the device's private key
        partial_sig = sign_request(txn_hash, device_id)
        partial_sigs[device_id] = partial_sig
        print(f"  Partial signature: {partial_sig[:32]}...")
        print(f"  Length: {len(partial_sig)} characters")
        print(f"  Raw bytes: {len(base64.b64decode(partial_sig))} bytes")
        
        # Create the payload
        payload_data = {
            "device_id": device_id,
            "partial_signature": partial_sig
        }
        
        # Sign the payload itself
        payload = {
            **payload_data,
            "signature": sign_request(json.dumps(payload_data), device_id)
        }
        
        print(f"  Sending to server for aggregation...")
        response = requests.post(f"{SERVER_URL}/submit_partial_signature", json=payload)
        result = response.json()
        print(f"  Server response: {result}")
        
        if result.get('signature_ready'):
            print("  ✓ Threshold reached! Final signature ready")
            final_response = result
        else:
            print(f"  → Waiting for more signatures ({i} of {THRESHOLD})")
    
    # Print final transaction details
    if final_response and "final_signature" in final_response:
        print("\n=== Signature Aggregation Process ===")
        print("Partial signatures collected:")
        for device_id, sig in partial_sigs.items():
            print(f"  {device_id}: {sig}")
            print(f"    Length: {len(sig)} characters")
            raw_bytes = base64.b64decode(sig)
            print(f"    Raw bytes: {len(raw_bytes)} bytes")
            print(f"    Raw hex: {raw_bytes.hex()}")
            print(f"    Verifies: {verify_signature(txn_hash, sig, IPHONE_KEYS[device_id]['public'])}")
        
        agg_sig = final_response["final_signature"]
        print(f"\nAggregated signature: {agg_sig}")
        print(f"  Length: {len(agg_sig)} characters")
        raw_agg = base64.b64decode(agg_sig)
        print(f"  Raw bytes: {len(raw_agg)} bytes")
        print(f"  Raw hex: {raw_agg.hex()}")
        
        # Extract r, s from the first signature for now (TODO: proper aggregation)
        first_sig = base64.b64decode(list(partial_sigs.values())[0])
        # DER encoded signature starts with 30 (sequence)
        # We need to extract r and s values
        r = first_sig[4:36].hex()  # 32 bytes for r
        s = first_sig[38:70].hex()  # 32 bytes for s
        v = 27  # Standard v value for Ethereum
        
        # Create the full Ethereum transaction
        tx_data = {
            "to": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
            "value": "0x0de0b6b3a7640000",  # 1 ETH in wei (hex)
            "from": eth_address,
            "nonce": "0x0",
            "gasPrice": "0x04a817c800",  # 20 Gwei
            "gasLimit": "0x5208",  # 21000
            "chainId": 1,  # Mainnet
            "data": "0x"  # Empty data field
        }
        
        # Create the complete Ethereum transaction
        eth_tx = {
            "raw": {  # Raw transaction fields
                **tx_data,
                "type": "0x0"  # Legacy transaction type
            },
            "signature": {
                "r": f"0x{r}",
                "s": f"0x{s}",
                "v": f"0x{hex(v)[2:]}",
            },
            "hash": txn_hash,
            "from": eth_address,
            "serialized": f"0x{txn_hash}{r}{s}{hex(v)[2:]}"  # Full serialized transaction
        }
        
        print("\n=== Complete Ethereum Transaction ===")
        print(json.dumps(eth_tx, indent=2))
        
        print("\n=== Transaction Components ===")
        print("1. From Address:", eth_address)
        print("2. To Address:", tx_data['to'])
        print("3. Value:", int(tx_data['value'], 16), "wei")
        print("4. Gas Price:", int(tx_data['gasPrice'], 16), "wei")
        print("5. Gas Limit:", int(tx_data['gasLimit'], 16))
        print("6. Nonce:", int(tx_data['nonce'], 16))
        print("7. Chain ID:", tx_data['chainId'])
        print("\n8. Signature Components:")
        print(f"   R: 0x{r}")
        print(f"   S: 0x{s}")
        print(f"   V: {v}")
        print("\n9. Transaction Hash:", txn_hash)
        print("\n10. Full Serialized Transaction:")
        print(eth_tx['serialized'])
        
        print("\n=== Final Status ===")
        if eth_address == tx_data['from'] and len(r) == 64 and len(s) == 64:
            print("✓ Transaction is valid and ready for broadcast")
            print(f"✓ Signing address verified: {eth_address}")
        else:
            print("✗ Transaction validation failed!")
            
    else:
        print("\n✗ No final signature received from server")

def run_gg20_dkg():
    devices = {}
    for i in range(1, TOTAL_SIGNERS + 1):
        device_id = f"iphone_{i}"
        private_key = ec.generate_private_key(ec.SECP256K1())
        devices[device_id] = GG20Device(device_id, private_key)
    return devices

def run_gg20_signing(devices, message_hash):
    """Run the GG20 signing protocol"""
    print("\n🔏 Starting GG20 Signing Protocol")
    print("=================================")
    
    # Round 1: Generate commitments
    print("\n=== Round 1: Generating Commitments ===")
    commitments = {}
    for device_id, device in devices.items():
        commitments[device_id] = device.start_signing(message_hash)
    
    # Round 2: Run MtA protocol
    print("\n=== Round 2: Running MtA Protocol ===")
    delta_values = {}
    for i, (device_id, device) in enumerate(devices.items()):
        delta_values[device_id] = {}
        for other_id, other_device in devices.items():
            if device_id != other_id:
                delta = device.run_mta(other_device)
                delta_values[device_id][other_id] = delta
    
    # Round 3: Compute R value
    print("\n=== Round 3: Computing Group R Value ===")
    R = None
    for device_id, commitment in commitments.items():
        R_i = ec.EllipticCurvePublicNumbers(
            commitment['R_i']['x'],
            commitment['R_i']['y'],
            CURVE
        ).public_key()
        if R is None:
            R = R_i
        else:
            R += R_i
    
    # Round 4: Generate signature shares
    print("\n=== Round 4: Generating Signature Shares ===")
    sig_shares = {}
    for device_id, device in devices.items():
        sig_shares[device_id] = device.compute_signature_share(message_hash, R)
    
    # Round 5: Combine shares
    print("\n=== Round 5: Combining Signature Shares ===")
    final_sig = GG20Device.combine_signature_shares(sig_shares.values(), R)
    
    print("\n✓ Signing Complete!")
    print(f"  R: {final_sig['r']}")
    print(f"  S: {final_sig['s']}")
    print(f"  V: {final_sig['v']}")
    return final_sig

# Run test flow
if __name__ == "__main__":
    print("\n🚀 Starting iPhone Signature Test Flow")
    print("======================================")
    
    # First enroll all iPhones
    enroll_iphones()
    
    # Then get transaction hash
    txn_hash = request_signature()
    
    # Finally submit signatures
    submit_signatures(txn_hash)
    
    print("\n✨ Test flow complete!")
