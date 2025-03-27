# thresh_demo

Threshold key distribution demo app. The intent is to securely shard an Ethereum key across multiple iOS devices, none of which ever have the full private key, and coordinate distributed partial signing from a server that also never knows the key. Signatures are then additive, and a final broadcastable ethereum transaction produced. In practice, backend would run in a TEE, for example AWS Nitro enclave to prevent modification. iOS devices would generate and store their partial keys in the secure enclave, non-exportable. No single location ever has the private key, and quorum approvals would be obtained from the iOS devices to sign for the single key. Transactions can be broken down and explained in detail, on a larger screen, such as an iPad.


```
(thresh_venv) cmc@cmc-pro thresh_demo % /Users/cmc/thresh_demo/thresh_venv/bin/python /Users/cmc/thresh_demo/test_client.py

🔐 Starting GG20 Protocol Implementation
=======================================
Start time: 2025-03-27 14:00:16
This implementation follows the GG20 paper (Gennaro-Goldfeder 2020)
for threshold ECDSA signatures on the secp256k1 curve.

=== Phase 1: Device Initialization ===
Creating virtual devices to simulate a distributed signing group:
  ✓ Initialized iphone_1
  ✓ Initialized iphone_2
  ✓ Initialized iphone_3
  ✓ Initialized iphone_4
  ✓ Initialized iphone_5

Group Configuration:
  • Total Signers: 5
  • Threshold Required: 3

=== Phase 2: Distributed Key Generation (DKG) ===
The DKG phase creates a shared group key where no single party knows the private key.

DKG Round 1: Generating and Sharing Key Material
Each device:
1. Generates a random polynomial of degree t-1
2. Creates commitments to the coefficients
3. Computes shares for all other participants

📱 iphone_1:

=== DKG Round 1 for iphone_1 ===
  ✓ Generated 5 shares
  ✓ Generated 3 commitments
  ✓ Generated polynomial of degree 2
  ✓ Created 3 commitments
  ✓ Computed 5 shares
  ✓ Submitted to coordination server

📱 iphone_2:

=== DKG Round 1 for iphone_2 ===
  ✓ Generated 5 shares
  ✓ Generated 3 commitments
  ✓ Generated polynomial of degree 2
  ✓ Created 3 commitments
  ✓ Computed 5 shares
  ✓ Submitted to coordination server

📱 iphone_3:

=== DKG Round 1 for iphone_3 ===
  ✓ Generated 5 shares
  ✓ Generated 3 commitments
  ✓ Generated polynomial of degree 2
  ✓ Created 3 commitments
  ✓ Computed 5 shares
  ✓ Submitted to coordination server

📱 iphone_4:

=== DKG Round 1 for iphone_4 ===
  ✓ Generated 5 shares
  ✓ Generated 3 commitments
  ✓ Generated polynomial of degree 2
  ✓ Created 3 commitments
  ✓ Computed 5 shares
  ✓ Submitted to coordination server

📱 iphone_5:

=== DKG Round 1 for iphone_5 ===
  ✓ Generated 5 shares
  ✓ Generated 3 commitments
  ✓ Generated polynomial of degree 2
  ✓ Created 3 commitments
  ✓ Computed 5 shares
  ✓ Submitted to coordination server

=== Phase 3: Signature Generation ===
The signing phase creates a threshold signature where any t parties can sign.

Message Details:
  • Raw message: 'Hello, GG20!'
  • Keccak256 hash: d1e074712321a4cd3f108005f24d453216dd0cd47a4ca52ac594d157f2a50c33

Signing Round 1: Commitment Generation
Each device generates random values and commitments for the MtA protocol:

📱 iphone_1:

=== Signing Round 1 for iphone_1 ===
  ✓ Generated random values
  ✓ Created commitments
  ✓ Generated random k_i and gamma_i
  ✓ Created R_i commitment: (102644869327326902790232915415384549853863779308576056699977035245126452402561, 62549515942209034264439026209688795820393241338961977308252466582895967031149)
  ✓ Created Gamma_i commitment
  ✓ Submitted commitments to server

📱 iphone_2:

=== Signing Round 1 for iphone_2 ===
  ✓ Generated random values
  ✓ Created commitments
  ✓ Generated random k_i and gamma_i
  ✓ Created R_i commitment: (39718147414795379613036622905659640127492818825000153494890769252366181092172, 68082659269891225622069612932403973277137802915819873964246853634250652248737)
  ✓ Created Gamma_i commitment
  ✓ Submitted commitments to server

📱 iphone_3:

=== Signing Round 1 for iphone_3 ===
  ✓ Generated random values
  ✓ Created commitments
  ✓ Generated random k_i and gamma_i
  ✓ Created R_i commitment: (56786487109451529458369448879168989302496324357335451499127442563524373840983, 84347053179693670996842034523660012672199454283520622632840466898856239761933)
  ✓ Created Gamma_i commitment
  ✓ Submitted commitments to server

📱 iphone_4:

=== Signing Round 1 for iphone_4 ===
  ✓ Generated random values
  ✓ Created commitments
  ✓ Generated random k_i and gamma_i
  ✓ Created R_i commitment: (32061584667105892192787774824953035013652818994572990662069908303763002126981, 45780300312782940244726277076793176371725263302969687867038815723760769704003)
  ✓ Created Gamma_i commitment
  ✓ Submitted commitments to server

📱 iphone_5:

=== Signing Round 1 for iphone_5 ===
  ✓ Generated random values
  ✓ Created commitments
  ✓ Generated random k_i and gamma_i
  ✓ Created R_i commitment: (77738560224045933543246227858482355307106907703625572600501953462854158746802, 28091756167580067210047010803357736743881006746039944910752235351727275260157)
  ✓ Created Gamma_i commitment
  ✓ Submitted commitments to server

Signing Round 2: Multiplicative-to-Additive (MtA) Conversion
Devices perform pairwise MtA protocol to compute signature shares:

📱 iphone_1 MtA interactions:
  • With iphone_2:
  Running MtA with iphone_2...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_3:
  Running MtA with iphone_3...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_4:
  Running MtA with iphone_4...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_5:
  Running MtA with iphone_5...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value

📱 iphone_2 MtA interactions:
  • With iphone_1:
  Running MtA with iphone_1...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_3:
  Running MtA with iphone_3...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_4:
  Running MtA with iphone_4...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_5:
  Running MtA with iphone_5...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value

📱 iphone_3 MtA interactions:
  • With iphone_1:
  Running MtA with iphone_1...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_2:
  Running MtA with iphone_2...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_4:
  Running MtA with iphone_4...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_5:
  Running MtA with iphone_5...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value

📱 iphone_4 MtA interactions:
  • With iphone_1:
  Running MtA with iphone_1...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_2:
  Running MtA with iphone_2...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_3:
  Running MtA with iphone_3...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_5:
  Running MtA with iphone_5...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value

📱 iphone_5 MtA interactions:
  • With iphone_1:
  Running MtA with iphone_1...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_2:
  Running MtA with iphone_2...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_3:
  Running MtA with iphone_3...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value
  • With iphone_4:
  Running MtA with iphone_4...
  ✓ MtA protocol complete
    ✓ Computed and shared delta value

=== Phase 4: Key Derivation ===
Computing group public key and Ethereum address...
1. Combining public shares from all participants
2. Performing point addition on secp256k1 curve

  • Processing iphone_1's public share:
    Point: (0xe2eeefee744b6cc38dd11990a844a9ad6fc21e4859e8ea383392fbe265c65981, 0x8a49c57c8dba7aa123d3b1c60c01dca3c0c5db5035c51d88546f2a5d74534f6d)
    ✓ Set as initial point

  • Processing iphone_2's public share:
    Point: (0x57cfacbed94391a49dbaf7bd941830c3d41cdf28e0819b065946037c90424b4c, 0x96856b6930bbc60f7cc348e9c1f8a46d075dfb57afce769890777c6c33d3eaa1)
    ✓ Added to group key using EC point addition

  • Processing iphone_3's public share:
    Point: (0x7d8c03409f833522e1e8e5d9ce04416add69af3773bfb8f039ac8da8b4550457, 0xba7abd8476fc569dbaa5484482992a8a7bba667221da62c5723e003941550a0d)
    ✓ Added to group key using EC point addition

  • Processing iphone_4's public share:
    Point: (0x46e236be7aeae96cb543e197d3bb1c2b848bca13e80d8fe9f3fd8f5b13987285, 0x6536bb530142482637650fe2a0fecff3bc90a4fe3ecdbfcbeb5f69e6cb3e2043)
    ✓ Added to group key using EC point addition

  • Processing iphone_5's public share:
    Point: (0xabde77414941965d7b27dada50a9522be5a564c296b76d933333153c4a5d84b2, 0x3e1b5edb9a9f4752bad62ca3217a0c7e7553e80809a0d175c4a94032c00438fd)
    ✓ Added to group key using EC point addition

=== Final Key Material ===
Group Public Key:
  • X coordinate: 0xe26c13c9308a920fd90ca4fcadc8aa1a485d3f2a5334cfe030a3f3abd3609252
  • Y coordinate: 0xa1b8f2af952b29feb3707db639a1d39a5dd256ae56ce54fe8a70de8b372f52d4
  • Raw bytes (hex): 04e26c13c9308a920fd90ca4fcadc8aa1a485d3f2a5334cfe030a3f3abd3609252a1b8f2af952b29feb3707db639a1d39a5dd256ae56ce54fe8a70de8b372f52d4
  • Derived Ethereum address: 0x59FDCeF9C08A5a455a66f9F1F0802B40a8409171

=== Phase 5: Transaction Construction ===
Transaction Details:
{
  "to": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "value": "0x0de0b6b3a7640000",
  "from": "0x59FDCeF9C08A5a455a66f9F1F0802B40a8409171",
  "nonce": "0x0",
  "gasPrice": "0x04a817c800",
  "gasLimit": "0x5208",
  "chainId": 1,
  "data": "0x"
}

=== Protocol Summary ===
✓ Successfully completed GG20 threshold signature setup:
  • 5 devices participated in the protocol
  • 3 signatures required for threshold
  • Wallet address: 0x59FDCeF9C08A5a455a66f9F1F0802B40a8409171
  • Transaction value: 1.00 ETH
  • Estimated gas cost: 420000.000000 ETH

Timing Information:
  • Start time: 2025-03-27 14:00:16.101
  • End time: 2025-03-27 14:00:16.248
  • Total duration: 0.147 seconds

🎉 GG20 Protocol Complete!
```
