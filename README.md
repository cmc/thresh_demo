# GG20 Threshold ECDSA Implementation

This implementation follows the GG20 protocol for threshold ECDSA signatures, allowing a group of participants to collectively sign Ethereum transactions without any single party having access to the private key.

## Overview

The system consists of two main components:
1. A central server that coordinates the signing ceremony and assembles the final signature
2. Multiple client devices that participate in the distributed key generation (DKG) and signing process

### Protocol Compliance

This implementation follows the GG20 protocol (Gennaro & Goldfeder 2020) which provides:
- Threshold ECDSA signatures without trusted dealers
- Security against malicious adversaries
- No single party ever has access to the private key
- Efficient signing with minimal rounds of communication

## Docker 

Build and run the server:
docker build -t gg20-server -f server/Dockerfile .
docker run -p 5010:5010 gg20-server

Build and run the client:
docker build -t gg20-client -f client/Dockerfile .
docker run --network host gg20-client --test-ceremony --num-devices 3

## Components

### Server (`server.py`)

The server acts as the coordinator and final assembler:

1. **DKG Phase**
   - Initiates the DKG ceremony
   - Provides the target EOA address to sign for
   - Collects shares and commitments from all participants
   - Validates the DKG process

2. **Signing Phase**
   - Initiates signing ceremony with a specific transaction
   - Collects commitments from all participants
   - Manages the MtA (Multiplicative-to-Additive) protocol
   - Combines partial signatures to create the final ECDSA signature
   - Assembles and outputs the final Ethereum transaction

3. **Transaction Management**
   - Stores transaction templates
   - Handles proper formatting of transaction fields
   - Outputs the final signed transaction in both JSON and hex formats

### Client (`client.py`)

Each client represents a participant in the threshold signature scheme:

1. **DKG Participation**
   - Generates polynomial coefficients
   - Creates and distributes shares
   - Stores key material per EOA
   - Validates received shares

2. **Signing Participation**
   - Generates partial signatures
   - Participates in MtA protocol
   - Never has access to complete private key
   - Maintains separation of signing material

## Protocol Flow

1. **DKG Initialization**
   ```
   Server → Clients: Start DKG with target EOA
   Clients → Server: Submit shares and commitments
   ```

2. **Signing Ceremony**
   ```
   Server → Clients: Start signing with transaction details
   Clients → Server: Submit signing commitments
   Clients ↔ Clients: MtA protocol (via server)
   Server: Combines shares and generates final signature
   ```

3. **Final Transaction**
   ```
   Server: Assembles complete transaction
   Server: Outputs broadcastable transaction hex
   ```

## Threat Model & Security Analysis

### Key Material Distribution

| Component | What it has | What it doesn't have | Why it's secure |
|-----------|-------------|---------------------|-----------------|
| Server | - Final signature (r,s,v)<br>- Transaction details<br>- Combined public key | - Private key shares<br>- Individual k values<br>- Gamma values | - Only combines final values<br>- Never sees raw shares<br>- Cannot derive private key from signature |
| Client 1 | - Own private key share<br>- Own k_i value<br>- Own gamma_i value | - Other clients' shares<br>- Combined private key<br>- Final k value | - Polynomial sharing prevents reconstruction<br>- MtA protocol hides intermediate values |
| Client 2 | - Own private key share<br>- Own k_i value<br>- Own gamma_i value | - Other clients' shares<br>- Combined private key<br>- Final k value | - Same as Client 1 |
| Client n | - Own private key share<br>- Own k_i value<br>- Own gamma_i value | - Other clients' shares<br>- Combined private key<br>- Final k value | - Same as Client 1 |

### Attack Vector Analysis

| Attack Vector | Protection Mechanism | Security Guarantee |
|---------------|---------------------|-------------------|
| Server Compromise | - No private key material stored<br>- Only handles public values | Even if compromised, attacker cannot generate new signatures |
| Single Client Compromise | - Threshold cryptography<br>- Share distribution | Compromised client cannot reconstruct key or generate signatures |
| Network Sniffing | - MtA protocol<br>- Secure channels | Intercepted communications don't reveal key material |
| Replay Attacks | - Per-transaction k values<br>- Unique gamma values | Each signature uses fresh randomness |
| Rogue Key Attack | - Commitment scheme<br>- Share verification | Clients cannot manipulate key generation |

### Key Security Properties

1. **Share Distribution**
   - Each client only has its own share
   - Minimum t+1 shares needed for reconstruction
   - Shares are refreshed per signing session

2. **Signing Process Security**
   ```
   Client i:
   - Has: k_i, γ_i, share_i
   - Cannot derive: k, γ, private_key
   ```

3. **MtA Protocol Security**
   - Prevents learning of intermediate values
   - Ensures multiplicative relationship
   - Preserves share secrecy

4. **Transaction Signing**
   ```
   k = Σ k_i mod n        (no party knows full k)
   γ = Σ γ_i mod n       (no party knows full γ)
   s = k^(-1)(m + rγ)    (computed distributively)
   ```

5. **Key Reconstruction Prevention**
   - No party ever sees complete private key
   - Each share is necessary but insufficient
   - Polynomial degree prevents collusion

### Security Assumptions

1. **Network**
   - Secure communication channels
   - Authenticated connections
   - Synchronous communication

2. **Adversary Model**
   - Malicious adversary
   - Cannot control t+1 parties
   - Computationally bounded

3. **Cryptographic**
   - DDH assumption in secp256k1
   - Random Oracle Model
   - Discrete Log hardness

## Command Line Arguments

### Server Arguments
- `--port`: Port to run server on (default: 5010)
- `--host`: Host address to bind to (default: 0.0.0.0)

### Client Arguments
- `--checkin`: Check in with server
- `--list-keys`: List stored EOAs and their key material
- `--show-device`: Show device information and configuration
- `--test-ceremony`: Run a test signing ceremony
- `--num-devices NUM_DEVICES`: Number of test devices to simulate in ceremony
- `-h, --help`: Show help message and exit

The client supports multiple modes of operation:
1. Device management (checkin, show info)
2. Key management (list stored keys)
3. Testing (run ceremony with simulated devices)

