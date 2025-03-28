from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from eth_utils import keccak, to_checksum_address
import secrets
import base64
import json
import requests
import os
import uuid
import argparse
from datetime import datetime
import time

# Constants
CURVE = ec.SECP256K1()
CURVE_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# Generator point for secp256k1
G = ec.generate_private_key(CURVE).public_key().public_numbers()
GENERATOR = ec.EllipticCurvePublicNumbers(G.x, G.y, CURVE).public_key()

SERVER_URL = "http://localhost:5010"
THRESHOLD = 3
TOTAL_SIGNERS = 5
CONFIG_FILE = "config.json"
ENCLAVE_STATE_FILE = "enclave_sim.json"
TEST_DEVICES_FILE = "test_devices.json"

class GG20Device:
    def __init__(self, device_id):
        self.device_id = device_id
        self.round = 0
        # Secret values
        self.secret_share = None
        self.k_i = None  # Random value for signing
        self.gamma_i = None  # Random value for MtA
        self.w_i = None  # Random value for MtA
        # Public values
        self.public_shares = {}  # {device_id: public_share}
        self.commitments = {}  # {device_id: commitment}
        self.R = None  # Combined R value for signing
        
    def generate_dkg_round1(self):
        """Round 1 of DKG: Generate shares and commitments"""
        print(f"\n=== DKG Round 1 for {self.device_id} ===")
        
        # Generate random polynomial coefficients
        coeffs = [secrets.randbelow(CURVE_ORDER) for _ in range(THRESHOLD)]
        self.coeffs = coeffs
        
        # Generate shares for each participant
        shares = {}
        commitments = []
        
        # Generate commitment to polynomial coefficients
        for coeff in coeffs:
            # Generate point commitment
            key = ec.derive_private_key(coeff, CURVE)
            point = key.public_key().public_numbers()
            commitments.append({
                'x': point.x,
                'y': point.y
            })
        
        # Generate shares for each participant
        for j in range(1, TOTAL_SIGNERS + 1):
            # Evaluate polynomial at point j
            share = coeffs[0]  # First coefficient is the secret
            for i in range(1, THRESHOLD):
                share = (share + coeffs[i] * pow(j, i, CURVE_ORDER)) % CURVE_ORDER
            
            shares[f"iphone_{j}"] = share
        
        print(f"  ✓ Generated {len(shares)} shares")
        print(f"  ✓ Generated {len(commitments)} commitments")
        
        return {
            'shares': shares,
            'commitments': commitments
        }
    
    def verify_share(self, from_id, share, commitments):
        """Verify a share using Feldman's VSS"""
        print(f"  Verifying share from {from_id}...")
        
        # Convert commitments back to points
        commitment_points = []
        for comm in commitments:
            point = ec.EllipticCurvePublicNumbers(
                comm['x'], comm['y'], CURVE
            ).public_key()
            commitment_points.append(point)
        
        # Verify the share against commitments
        my_index = int(self.device_id.split('_')[1])
        lhs = ec.derive_private_key(share, CURVE).public_key()
        
        rhs = commitment_points[0]
        for i in range(1, len(commitment_points)):
            # Use scalar multiplication properly
            scalar = pow(my_index, i, CURVE_ORDER)
            temp_key = ec.derive_private_key(scalar, CURVE)
            rhs = rhs.public_numbers().x + temp_key.public_key().public_numbers().x
        
        if lhs.public_numbers().x == rhs:
            print("  ✓ Share verified successfully")
            return True
        else:
            print("  ✗ Share verification failed!")
            return False
    
    def start_signing(self, message_hash):
        """Round 1 of GG20 signing: Generate k_i and gamma_i"""
        print(f"\n=== Signing Round 1 for {self.device_id} ===")
        
        # Generate random k_i and gamma_i
        self.k_i = secrets.randbelow(CURVE_ORDER)
        self.gamma_i = secrets.randbelow(CURVE_ORDER)
        self.w_i = secrets.randbelow(CURVE_ORDER)
        
        # Compute R_i = g^k_i and commitment
        self.R_i = ec.derive_private_key(self.k_i, CURVE).public_key()
        self.Gamma_i = ec.derive_private_key(self.gamma_i, CURVE).public_key()
        
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

def load_or_create_config():
    """Load existing config or create new one"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            print(f"✓ Loaded existing config with {len(config['devices'])} devices")
            return config
    else:
        config = {
            "created_at": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "devices": {},  # {device_name: {device_config, key_material}}
            "ceremonies": {}  # {ceremony_id: {participants, status, created_at}}
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f, indent=2)
            print("✓ Created new config")
        return config

class EnclaveClient:
    def __init__(self, device_name=None, config=None):
        self.device_name = device_name
        self.config = config or load_or_create_config()
        self.setup_device()
    
    def setup_device(self):
        """Setup or load device configuration"""
        if self.device_name:
            if self.device_name not in self.config['devices']:
                # Generate new device identity
                private_key = ec.generate_private_key(CURVE)
                public_key = private_key.public_key()
                
                # Serialize keys
                private_bytes = private_key.private_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PrivateFormat.PKCS8,
                    encryption_algorithm=serialization.NoEncryption()
                )
                public_bytes = public_key.public_bytes(
                    encoding=serialization.Encoding.PEM,
                    format=serialization.PublicFormat.SubjectPublicKeyInfo
                )
                
                # Create device entry
                self.config['devices'][self.device_name] = {
                    "device_config": {
                        "created_at": datetime.now().isoformat(),
                        "enclave_private_key": private_bytes.decode(),
                        "enclave_public_key": public_bytes.decode()
                    },
                    "key_material": {}  # {eth_address: {partial_key_data}}
                }
                self.save_config()
                print(f"✓ Created new device: {self.device_name}")
            else:
                print(f"✓ Loaded existing device: {self.device_name}")
    
    def save_config(self):
        """Save current configuration"""
        self.config["last_updated"] = datetime.now().isoformat()
        with open(CONFIG_FILE, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def store_key_material(self, eth_address, key_material):
        """Store key material for an EOA"""
        if self.device_name:
            self.config['devices'][self.device_name]['key_material'][eth_address] = {
                "created_at": datetime.now().isoformat(),
                "data": key_material
            }
            self.save_config()
            print(f"✓ Stored key material for {eth_address}")
    
    def get_key_material(self, eth_address):
        """Retrieve key material for an EOA"""
        if self.device_name:
            device_data = self.config['devices'][self.device_name]
            return device_data['key_material'].get(eth_address, {}).get('data')
        return None

    def checkin_with_server(self):
        """Register device with server and get pending signing requests"""
        print(f"\n=== Device Check-in: {self.device_name} ===")
        
        response = requests.post(f"{SERVER_URL}/enroll", json={
            "device_id": self.device_name,
            "public_key": self.config['devices'][self.device_name]['device_config']['enclave_public_key']
        })
        
        if response.status_code == 200:
            print("✓ Successfully checked in with server")
            # Handle any pending signing requests
            return response.json().get("pending_requests", [])
        else:
            print("✗ Failed to check in with server")
            return []
    
    def participate_in_signing(self, eth_address, message_hash):
        """Participate in GG20 signing for a specific EOA"""
        key_material = self.get_key_material(eth_address)
        if not key_material:
            print(f"✗ No key material found for {eth_address}")
            return None
        
        print(f"\n=== Signing for {eth_address} ===")
        # Use stored key material to generate partial signature
        # ... GG20 signing logic here ...
        
        return "partial_signature"  # Replace with actual partial signature

    def generate_dkg_round1(self):
        """Round 1 of DKG: Generate shares and commitments"""
        print(f"\n=== DKG Round 1 for {self.device_name} ===")
        
        # Get target EOA from server
        response = requests.post(f"{SERVER_URL}/dkg/start")
        if response.status_code != 200:
            print("Failed to start DKG")
            return None
        
        target_eoa = response.json()['target_eoa']
        print(f"  • Target EOA address: {target_eoa}")
        
        # Check if we already have key material for this EOA
        if target_eoa in self.config['devices'][self.device_name]['key_material']:
            print(f"  • Using existing key material for {target_eoa}")
            key_material = self.config['devices'][self.device_name]['key_material'][target_eoa]
            coeffs = [int(c) for c in key_material['polynomial_coeffs']]
        else:
            # Generate new key material
            print(f"  • Generating new key material for {target_eoa}")
            coeffs = [secrets.randbelow(CURVE_ORDER) for _ in range(THRESHOLD)]
            key_material = {
                'polynomial_coeffs': [str(c) for c in coeffs],
                'share_index': int(self.device_name.split('_')[1]),
                'group_public_key': None,  # Will be set later
                'partial_private_key': str(coeffs[0]),  # First coefficient is the share
                'created_at': datetime.now().isoformat()
            }
            self.config['devices'][self.device_name]['key_material'][target_eoa] = key_material
            self.save_config()
            print(f"  ✓ Stored new key material")
        
        # Generate shares and commitments using coeffs
        shares = {}
        commitments = []
        
        # Generate commitment to polynomial coefficients
        for coeff in coeffs:
            # Generate point commitment
            key = ec.derive_private_key(coeff, CURVE)
            point = key.public_key().public_numbers()
            commitments.append({
                'x': point.x,
                'y': point.y
            })
        
        # Generate shares for each participant
        for j in range(1, TOTAL_SIGNERS + 1):
            # Evaluate polynomial at point j
            share = coeffs[0]  # First coefficient is the secret
            for i in range(1, THRESHOLD):
                share = (share + coeffs[i] * pow(j, i, CURVE_ORDER)) % CURVE_ORDER
            
            shares[f"device_{j}"] = share
        
        print(f"  ✓ Generated {len(shares)} shares")
        print(f"  ✓ Generated {len(commitments)} commitments")
        
        return {
            'shares': shares,
            'commitments': commitments,
            'target_eoa': target_eoa
        }

    def start_signing(self, message_hash, target_eoa):
        """Round 1 of GG20 signing: Generate k_i and gamma_i"""
        print(f"\n=== Signing Round 1 for {self.device_name} ===")
        print(f"  • Signing for EOA: {target_eoa}")
        print(f"  • Message hash: {message_hash}")
        
        # Get stored key material for this EOA
        key_material = self.config['devices'][self.device_name]['key_material'].get(target_eoa)
        if not key_material:
            print(f"✗ No key material found for {target_eoa}")
            return None
        
        # Generate random k_i and gamma_i for this signing session
        self.k_i = secrets.randbelow(CURVE_ORDER)
        self.gamma_i = secrets.randbelow(CURVE_ORDER)
        
        # Create commitment to send to server
        self.R_i = ec.derive_private_key(self.k_i, CURVE).public_key()
        
        commitment = {
            'k_i': hex(self.k_i),
            'gamma_i': hex(self.gamma_i),
            'R_i': {
                'x': self.R_i.public_numbers().x,
                'y': self.R_i.public_numbers().y
            }
        }
        
        print("  ✓ Generated partial signature data")
        return commitment

    def run_mta(self, other_device):
        """Run Multiplicative to Additive (MtA) protocol with another device"""
        print(f"  Running MtA with {other_device.device_name}...")
        
        # MtA for k_i * gamma_j
        alpha_ij = secrets.randbelow(CURVE_ORDER)
        beta_ij = secrets.randbelow(CURVE_ORDER)
        
        # Simulate secure two-party computation
        delta_ij = (self.k_i * other_device.gamma_i + alpha_ij + beta_ij) % CURVE_ORDER
        
        print("  ✓ MtA protocol complete")
        return delta_ij

def create_test_devices(num_devices):
    """Create and store test devices"""
    config = load_or_create_config()
    devices = {}
    
    ceremony_id = f"ceremony_{uuid.uuid4().hex[:8]}"
    config['ceremonies'][ceremony_id] = {
        "created_at": datetime.now().isoformat(),
        "status": "in_progress",
        "participants": [],
        "threshold": THRESHOLD,
        "total_signers": num_devices
    }
    
    for i in range(1, num_devices + 1):
        device_name = f"device_{i}"
        device = EnclaveClient(device_name, config)
        devices[device_name] = device
        config['ceremonies'][ceremony_id]['participants'].append(device_name)
        print(f"✓ Added {device_name} to ceremony {ceremony_id}")
    
    # Save updated config
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    return devices, ceremony_id

def run_signing_ceremony(devices):
    """Run complete GG20 signing ceremony with all devices"""
    start_time = time.time()
    
    print("\n🔐 Starting GG20 Signing Ceremony")
    print("================================")
    print(f"Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Start DKG
    print("\n=== Phase 1: Distributed Key Generation ===")
    response = requests.post(f"{SERVER_URL}/dkg/start")
    if response.status_code != 200:
        print("Failed to start DKG")
        return None
    
    dkg_data = response.json()
    target_eoa = dkg_data.get('target_eoa')
    transaction = dkg_data.get('transaction')
    
    if not target_eoa or not transaction:
        print("Missing required data from server")
        print(f"Server response: {dkg_data}")
        return None
    
    print(f"\nTransaction to sign:")
    print(f"  • From: {target_eoa}")
    print(f"  • To: {transaction['to']}")
    print(f"  • Value: {int(transaction['value'], 16) / 1e18:.6f} ETH")
    print(f"  • Gas Price: {int(transaction['gasPrice'], 16) / 1e9:.1f} Gwei")
    print(f"  • Gas Limit: {int(transaction['gas'], 16)}")
    print(f"  • Chain ID: {transaction['chainId']}")
    
    # Run DKG Round 1
    for device_name, device in devices.items():
        dkg_data = device.generate_dkg_round1()
        if not dkg_data:
            print("Failed to generate DKG data")
            return None
        response = requests.post(f"{SERVER_URL}/dkg/submit", json={
            "device_id": device_name,
            "commitments": dkg_data["commitments"],
            "shares": dkg_data["shares"]
        })
        print(f"✓ {device_name} submitted DKG data")
    
    # Get signing request from server
    print(f"\n=== Phase 2: Signature Generation ===")
    response = requests.post(f"{SERVER_URL}/signing/start")
    if response.status_code != 200:
        print("Failed to get signing request")
        return None
    
    signing_data = response.json()
    message_hash = signing_data['message_hash']
    target_eoa = signing_data['target_eoa']
    
    # Run signing protocol
    for device_name, device in devices.items():
        commitment = device.start_signing(message_hash, target_eoa)
        if not commitment:
            print(f"✗ {device_name} failed to generate commitment")
            return None
        response = requests.post(f"{SERVER_URL}/signing/commit", json={
            "device_id": device_name,
            "commitment": commitment
        })
        print(f"✓ {device_name} submitted commitment")
    
    # Run MtA protocol
    print("\n=== Phase 3: MtA Protocol ===")
    for device_name, device in devices.items():
        for other_name, other_device in devices.items():
            if device_name != other_name:
                print(f"  Running MtA with {other_name}...")
                delta = device.run_mta(other_device)
                response = requests.post(f"{SERVER_URL}/signing/mta", json={
                    "from": device_name,
                    "to": other_name,
                    "delta": delta
                })
                print(f"  ✓ MtA protocol complete")
                print(f"✓ {device_name} completed MtA with {other_name}")
    
    end_time = time.time()
    duration = end_time - start_time
    
    print(f"\nTotal duration: {duration:.2f} seconds")
    
    # Store ceremony info
    config = load_or_create_config()
    ceremony_id = f"ceremony_{secrets.token_hex(4)}"
    config['ceremonies'][ceremony_id] = {
        'started_at': datetime.now().isoformat(),
        'duration': duration,
        'message_hash': message_hash
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"\nCeremony ID: {ceremony_id}")
    print(f"Message hash: {message_hash}")
    
    return {
        'ceremony_id': ceremony_id,
        'message_hash': message_hash,
        'duration': duration
    }

def main():
    parser = argparse.ArgumentParser(description="GG20 Enclave Client")
    parser.add_argument('--checkin', action='store_true', help='Check in with server')
    parser.add_argument('--list-keys', action='store_true', help='List stored EOAs')
    parser.add_argument('--show-device', action='store_true', help='Show device info')
    parser.add_argument('--test-ceremony', action='store_true', help='Run test signing ceremony')
    parser.add_argument('--num-devices', type=int, default=TOTAL_SIGNERS, help='Number of test devices')
    args = parser.parse_args()

    if args.test_ceremony:
        devices, ceremony_id = create_test_devices(args.num_devices)
        result = run_signing_ceremony(devices)
        if result:
            print(f"\nCeremony ID: {ceremony_id}")
            print(f"Message hash: {result['message_hash']}")
            
            # Update ceremony status
            config = load_or_create_config()
            config['ceremonies'][ceremony_id].update({
                'status': "completed",
                'message_hash': result['message_hash'],
                'completed_at': datetime.now().isoformat()
            })
            with open(CONFIG_FILE, 'w') as f:
                json.dump(config, f, indent=2)
    
    if args.show_device:
        config = load_or_create_config()
        print("\n=== Device Information ===")
        for device_name, device_data in config['devices'].items():
            print(f"\n• {device_name}:")
            print(f"  Created: {device_data['device_config']['created_at']}")
            print(f"  Public Key: {device_data['device_config']['enclave_public_key'][:64]}...")
            print(f"  EOAs: {len(device_data['key_material'])}")
        
        print("\n=== Ceremonies ===")
        for ceremony_id, ceremony_data in config['ceremonies'].items():
            print(f"\n• {ceremony_id}:")
            print(f"  Status: {ceremony_data['status']}")
            print(f"  Created: {ceremony_data['created_at']}")
            print(f"  Participants: {len(ceremony_data['participants'])}")
            if 'completed_at' in ceremony_data:
                print(f"  Completed: {ceremony_data['completed_at']}")
    
    if args.list_keys:
        config = load_or_create_config()
        print("\n=== Stored EOAs ===")
        for device_name, device_data in config['devices'].items():
            print(f"\n• {device_name}:")
            for eth_address, key_data in device_data['key_material'].items():
                print(f"  - {eth_address} (created: {key_data['created_at']})")
    
    if args.checkin:
        config = load_or_create_config()
        print("\nChecking in all devices:")
        for device_name in config['devices']:
            client = EnclaveClient(device_name, config)
            pending_requests = client.checkin_with_server()
            print(f"\n• {device_name}:")
            if pending_requests:
                print("  Pending Requests:")
                for req in pending_requests:
                    print(f"  - Request for {req['eth_address']}")
                    client.participate_in_signing(req['eth_address'], req['message_hash'])
            else:
                print("  No pending requests")

if __name__ == "__main__":
    main()
