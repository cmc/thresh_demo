# thresh_demo

Threshold key distribution demo app. The intent is to securely shard an Ethereum key across multiple iOS devices, none of which ever have the full private key, and coordinate distributed partial signing from a server that also never knows the key. Signatures are then additive, and a final broadcastable ethereum transaction produced. In practice, backend would run in a TEE, for example AWS Nitro enclave to prevent modification. iOS devices would generate and store their partial keys in the secure enclave, non-exportable. No single location ever has the private key, and quorum approvals would be obtained from the iOS devices to sign for the single key. Transactions can be broken down and explained in detail, on a larger screen, such as an iPad.


```

🔐 Starting GG20 Protocol Implementation
=======================================
Start time: 2025-03-27 14:03:04
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
  ✓ Created R_i commitment: (12509718238990874994231972674246360288630510561556088998713841222227628363318, 105699008751847324186841964389751325457291081390959724499981886015929974550115)
  ✓ Created Gamma_i commitment
  ✓ Submitted commitments to server

📱 iphone_2:

=== Signing Round 1 for iphone_2 ===
  ✓ Generated random values
  ✓ Created commitments
  ✓ Generated random k_i and gamma_i
  ✓ Created R_i commitment: (35444030597927868027741284831673055976225639901695290373354575823922400427619, 62141418185457254162200640870500789809114383527864980829140253721363249457756)
  ✓ Created Gamma_i commitment
  ✓ Submitted commitments to server

📱 iphone_3:

=== Signing Round 1 for iphone_3 ===
  ✓ Generated random values
  ✓ Created commitments
  ✓ Generated random k_i and gamma_i
  ✓ Created R_i commitment: (78098043006864541614503953765398246539590685801342034998926616284383152880218, 59517468360601733580118983864586276043808349568171210138787809652392816435317)
  ✓ Created Gamma_i commitment
  ✓ Submitted commitments to server

📱 iphone_4:

=== Signing Round 1 for iphone_4 ===
  ✓ Generated random values
  ✓ Created commitments
  ✓ Generated random k_i and gamma_i
  ✓ Created R_i commitment: (42995165327557740073165684086320565888282085898348927019091374159555603190088, 31931780498891668229043327172177259402735676432681847382938532524850073020810)
  ✓ Created Gamma_i commitment
  ✓ Submitted commitments to server

📱 iphone_5:

=== Signing Round 1 for iphone_5 ===
  ✓ Generated random values
  ✓ Created commitments
  ✓ Generated random k_i and gamma_i
  ✓ Created R_i commitment: (52025020619863530057264569310891484697729986085453848706289815869645846320482, 78523048673215814347970493855300286657558309718959688923670326071372948843812)
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
    Point: (0x1ba83fe65ab46f3a2fccc7d4fc6cba080326ac97a1f4107e4fadbe8148378e36, 0xe9af84d5d6d2fa85cb0427c9430fdfe273fb9c1dbe7b2a2d4d75dcd8938c6e63)
    ✓ Set as initial point

  • Processing iphone_2's public share:
    Point: (0x4e5c9c42fd6842079fec780114500999dfa41358767087a59f56a58ccd417e63, 0x8962cbd975996be1daa3c396249159a78af58361cbbec8c74dd4b248db396a5c)
    ✓ Added to group key using EC point addition

  • Processing iphone_3's public share:
    Point: (0xaca9ed06c6f1ce0aa79f71af14182606b7e624ba482ed031be5de59c8beaba5a, 0x8395b17d2a358abaa45e7e300ab98c362ff4e312345aa6ed02502f82660a6075)
    ✓ Added to group key using EC point addition

  • Processing iphone_4's public share:
    Point: (0x5f0e66b4d3f7a1907ca56a7f3b6f44e95ab7348e51b80c133aa1c49a0e77d148, 0x4698bf4e49f51c17c3d1ed2f313574b0b61b4b4cdac3af2e93db7dedf8d3a98a)
    ✓ Added to group key using EC point addition

  • Processing iphone_5's public share:
    Point: (0x73051e40ba76ef3a2bbfa72ca366fd771730f4464d325cb37ecbd2e5ccd59562, 0xad9a7877181d668f1acad2d9751d3063925371d9268735a98e3e5b04aea22d24)
    ✓ Added to group key using EC point addition

=== Final Key Material ===
Group Public Key:
  • X coordinate: 0x42812e2bb13fb9d4d027b3b3173c098059ce216b46ed5286021bcc2faf5cb58d
  • Y coordinate: 0xd970cac7351bfeb717f71c713314a1256f2cf8bd2d4c2bca0ebf67939832911b
  • Raw bytes (hex): 0442812e2bb13fb9d4d027b3b3173c098059ce216b46ed5286021bcc2faf5cb58dd970cac7351bfeb717f71c713314a1256f2cf8bd2d4c2bca0ebf67939832911b
  • Derived Ethereum address: 0x5e14BeCe06fa3515F380af7fC7A5bB5227b6b43a

=== Phase 5: Transaction Construction ===
Transaction Details:
{
  "to": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "value": "0x0de0b6b3a7640000",
  "from": "0x5e14BeCe06fa3515F380af7fC7A5bB5227b6b43a",
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
  • Wallet address: 0x5e14BeCe06fa3515F380af7fC7A5bB5227b6b43a
  • Transaction value: 1.00 ETH
  • Estimated gas cost: 420000.000000 ETH

Timing Information:
  • Start time: 2025-03-27 14:03:04.560
  • End time: 2025-03-27 14:03:04.709
  • Total duration: 0.148 seconds

🎉 GG20 Protocol Complete!

