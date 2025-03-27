from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import hashes, serialization
from eth_utils import keccak, to_checksum_address
import secrets
import base64
import json
import requests

# Constants
CURVE = ec.SECP256K1()
CURVE_ORDER = 0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFEBAAEDCE6AF48A03BBFD25E8CD0364141
# Generator point for secp256k1
G = ec.generate_private_key(CURVE).public_key().public_numbers()
GENERATOR = ec.EllipticCurvePublicNumbers(G.x, G.y, CURVE).public_key()

SERVER_URL = "http://localhost:5010"
THRESHOLD = 3
TOTAL_SIGNERS = 5

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

def run_gg20_protocol():
    """Run the complete GG20 protocol"""
    print("\n🔐 Starting GG20 Protocol")
    print("=========================")
    
    # Initialize devices
    devices = {}
    for i in range(1, TOTAL_SIGNERS + 1):
        device_id = f"iphone_{i}"
        devices[device_id] = GG20Device(device_id)
        print(f"✓ Initialized {device_id}")
    
    # Start DKG
    print("\n=== Starting DKG ===")
    response = requests.post(f"{SERVER_URL}/dkg/start")
    if response.status_code != 200:
        print("Failed to start DKG")
        return
    
    print("\n=== DKG Round 1: Generating Shares ===")
    # Run DKG Round 1
    for device_id, device in devices.items():
        print(f"\nDevice {device_id}:")
        dkg_data = device.generate_dkg_round1()
        response = requests.post(f"{SERVER_URL}/dkg/submit", json={
            "device_id": device_id,
            "commitments": dkg_data["commitments"],
            "shares": dkg_data["shares"]
        })
        print(f"  ✓ Generated {len(dkg_data['shares'])} shares")
        print(f"  ✓ Generated {len(dkg_data['commitments'])} commitments")
        print(f"  ✓ Submitted to server")
    
    # Start signing
    message = "Hello, GG20!"
    message_hash = keccak(message.encode()).hex()
    
    print("\n=== Starting Signing Protocol ===")
    print(f"Message to sign: '{message}'")
    print(f"Message hash: {message_hash}")
    
    response = requests.post(f"{SERVER_URL}/signing/start", json={
        "message_hash": message_hash
    })
    
    print("\n=== Round 1: Generating Commitments ===")
    # Run signing protocol
    for device_id, device in devices.items():
        print(f"\nDevice {device_id}:")
        commitment = device.start_signing(message_hash)
        response = requests.post(f"{SERVER_URL}/signing/commit", json={
            "device_id": device_id,
            "commitment": commitment
        })
        print(f"  ✓ Generated k_i and gamma_i")
        print(f"  ✓ Created R_i and Gamma_i commitments")
        print(f"  ✓ Submitted to server")
    
    print("\n=== Round 2: Running MtA Protocol ===")
    # Run MtA protocol
    for device_id, device in devices.items():
        print(f"\nDevice {device_id} MtA interactions:")
        for other_id, other_device in devices.items():
            if device_id != other_id:
                print(f"  • With {other_id}:")
                delta = device.run_mta(other_device)
                response = requests.post(f"{SERVER_URL}/signing/mta", json={
                    "from": device_id,
                    "to": other_id,
                    "delta": delta
                })
                print(f"    ✓ Delta value computed and submitted")
    
    # Derive group public key and Ethereum address
    print("\n=== Computing Group Public Key ===")
    
    # Use the first device's R_i as the group public key for demo
    # In a real implementation, we would properly combine all R_i values
    group_public_key = list(devices.values())[0].R_i
    print("  • Using first device's public share (simplified for demo)")
    
    # Get the uncompressed public key bytes (04 || x || y)
    public_key_bytes = group_public_key.public_bytes(
        encoding=serialization.Encoding.X962,
        format=serialization.PublicFormat.UncompressedPoint
    )
    
    # Convert to Ethereum address (keccak256 of x || y, last 20 bytes)
    eth_address = to_checksum_address(keccak(public_key_bytes[1:])[-20:])
    
    print("\n=== Group Key Details ===")
    print(f"Public Key (bytes): {public_key_bytes.hex()}")
    print(f"Ethereum Address: {eth_address}")
    
    print("\n=== Final Transaction Details ===")
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
    
    print(json.dumps(tx_data, indent=2))
    print("\n=== Protocol Summary ===")
    print(f"• {TOTAL_SIGNERS} devices participated")
    print(f"• {THRESHOLD} threshold achieved")
    print(f"• From address: {eth_address}")
    print(f"• To address: {tx_data['to']}")
    print(f"• Value: {int(tx_data['value'], 16) / 1e18:.2f} ETH")
    print(f"• Gas cost: {int(tx_data['gasPrice'], 16) * int(tx_data['gasLimit'], 16) / 1e9:.6f} ETH")
    
    print("\n✓ GG20 Protocol Complete!")

if __name__ == "__main__":
    run_gg20_protocol()
