# thresh_demo

Threshold key distribution demo app. The intent is to securely shard an Ethereum key across multiple iOS devices, none of which ever have the full private key, and coordinate distributed partial signing from a server that also never knows the key. Signatures are then additive, and a final broadcastable ethereum transaction produced. In practice, backend would run in a TEE, for example AWS Nitro enclave to prevent modification. iOS devices would generate and store their partial keys in the secure enclave, non-exportable. No single location ever has the private key, and quorum approvals would be obtained from the iOS devices to sign for the single key. Transactions can be broken down and explained in detail, on a larger screen, such as an iPad.


```
(thresh_venv) cmc@cmc-pro thresh_demo % /Users/cmc/thresh_demo/thresh_venv/bin/python /Users/cmc/thresh_demo/test_client.py

🚀 Starting iPhone Signature Test Flow
======================================

=== Enrolling iPhones with MPC Setup ===

Generating key material for iphone_1...
  Generating key shares...
  ✓ EC key share generated for signing
  ✓ RSA key generated for encryption
  EC Public share: -----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEHWW1DfpiAk9hWZ5z2Nt87tu4O33s/j/q
AWhiWk9hoAx86o1OkEQ3SfmCU2j5B6ptV6tjcdnmBk2nCA2hk2ZeXw==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAryP2Wfbqix5zdZC48/+g
BG91k8OyInrjzDSXhpMUr55+yUMZ20zwG/JJ6ZOc7nUMJg7P3jcrXByo1Qk2nsef
BrWPzc+/en5+6tTXHVYt1ziEGvo0frMshX3gGNw2C71Vbz69MG01ceEZe5BfTUQ+
8qTy/r0um9a5/mBIH+GSa/hiXir/0HIvBV64AzxhJ50MliuTGbToldtu/rTtO7cc
tsXoxYDpW+rg5ob0+fJoeSh+W/hjAJCMbC1/p3U9GKEXhgs/+AYNCkHTpOWvWhX8
UlZJZuww7IFJoLEA4lo3d72tSvT4cVb/Q8FwOws37NgjjHMyk8SOXfa3W5jtkKcy
/QIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_1...
  Data to sign: {"device_id": "iphone_1", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEHWW1DfpiAk9hWZ5z2Nt87tu4O33s/j/q\nAWhiWk9hoAx86o1OkEQ3SfmCU2j5B6ptV6tjcdnmBk2nCA2hk2ZeXw==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAryP2Wfbqix5zdZC48/+g\nBG91k8OyInrjzDSXhpMUr55+yUMZ20zwG/JJ6ZOc7nUMJg7P3jcrXByo1Qk2nsef\nBrWPzc+/en5+6tTXHVYt1ziEGvo0frMshX3gGNw2C71Vbz69MG01ceEZe5BfTUQ+\n8qTy/r0um9a5/mBIH+GSa/hiXir/0HIvBV64AzxhJ50MliuTGbToldtu/rTtO7cc\ntsXoxYDpW+rg5ob0+fJoeSh+W/hjAJCMbC1/p3U9GKEXhgs/+AYNCkHTpOWvWhX8\nUlZJZuww7IFJoLEA4lo3d72tSvT4cVb/Q8FwOws37NgjjHMyk8SOXfa3W5jtkKcy\n/QIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEQCIAprznVTimGRZm+ryEqHxXnHPtYH...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending enrollment request to server...
  Server response status: 200
  Server response: {'message': 'Device iphone_1 enrolled', 'status': 'success'}

Generating key material for iphone_2...
  Generating key shares...
  ✓ EC key share generated for signing
  ✓ RSA key generated for encryption
  EC Public share: -----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEuT3n5y0lu4T+9rJcG3xYEDeVi22RTSaA
IDHU8L/Yw2fB2ayfUcJMGs+mGj8ss+TnHkDf33aoGE6e+7HM4ORJ/w==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsjSfSNv6G8sXiFPytU80
O/VCL2q0QmaOJ3fcrxODu0dAgepliPkwCsKdeCW+nIIc2l6QuZzc7ZzLmswGrHhR
XGPGoqKHHjjVAZyD5g35oFvf+BElZoXqzyQG1D438o6UX1LAXnn8w0Ed8rzt2l9B
O3vNnb9EprtBg5Y9acDNqXCxj0ZTQKm1ox8Mkw3Nd2b2q2EerJhqRY3iLp98fkLd
GAzpsp57kevWGVoS9Jyj2WoA2nQKENUjvDe2s7va7qVFZjttpnVZAfGQhcC6bU2R
Brqvadwo0ADax5hnhmyBdn3uEs8+NI+9KnQf518rkfGGvBHPU9SuHWYTYN/erR6p
CQIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_2...
  Data to sign: {"device_id": "iphone_2", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEuT3n5y0lu4T+9rJcG3xYEDeVi22RTSaA\nIDHU8L/Yw2fB2ayfUcJMGs+mGj8ss+TnHkDf33aoGE6e+7HM4ORJ/w==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAsjSfSNv6G8sXiFPytU80\nO/VCL2q0QmaOJ3fcrxODu0dAgepliPkwCsKdeCW+nIIc2l6QuZzc7ZzLmswGrHhR\nXGPGoqKHHjjVAZyD5g35oFvf+BElZoXqzyQG1D438o6UX1LAXnn8w0Ed8rzt2l9B\nO3vNnb9EprtBg5Y9acDNqXCxj0ZTQKm1ox8Mkw3Nd2b2q2EerJhqRY3iLp98fkLd\nGAzpsp57kevWGVoS9Jyj2WoA2nQKENUjvDe2s7va7qVFZjttpnVZAfGQhcC6bU2R\nBrqvadwo0ADax5hnhmyBdn3uEs8+NI+9KnQf518rkfGGvBHPU9SuHWYTYN/erR6p\nCQIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEQCICYySL5ddb+6hnqzEJOE+2zlPFrp...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending enrollment request to server...
  Server response status: 200
  Server response: {'message': 'Device iphone_2 enrolled', 'status': 'success'}

Generating key material for iphone_3...
  Generating key shares...
  ✓ EC key share generated for signing
  ✓ RSA key generated for encryption
  EC Public share: -----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEvUN1ByJ7cXRhEnNG9XsQQ/UMEgxtYZ2u
FMSTSUgg4Nh9qJoAM2nyvDHZeZ26q8RDRaArFxChqeyzLQOCSa/tIg==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtvCiCl5Wywfsw5UBG/rL
9LqmX+VYY8PMJbhO+ToBNN8IaXJggQUklpY1rv2waNXyW5gSVsv9vfjGRozThU5A
XDB4dSBKdOMIzvzqeAT4GgCJvJi9XVF4qOYqsr5rIFmxOiZx5w818bsuC5a8fgBW
fmlmnA9xL2ZkR39Cg0kngW9WlvUdtXRKOaKjzi7NeiUs2XvTS/Gqmyxrs/jIaicX
TVkfm/UNks8c4Wi93RWDm06SVNm4JRhfZbE84PjE3fEJE4H3Eh3rS0V9NX3fzQa8
/Q7vCi0L4motLiGFr/GhMietcQwkMLa0hV3QoSdbSrxHdv45LJgntXpoXFA+YIoU
fQIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_3...
  Data to sign: {"device_id": "iphone_3", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEvUN1ByJ7cXRhEnNG9XsQQ/UMEgxtYZ2u\nFMSTSUgg4Nh9qJoAM2nyvDHZeZ26q8RDRaArFxChqeyzLQOCSa/tIg==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtvCiCl5Wywfsw5UBG/rL\n9LqmX+VYY8PMJbhO+ToBNN8IaXJggQUklpY1rv2waNXyW5gSVsv9vfjGRozThU5A\nXDB4dSBKdOMIzvzqeAT4GgCJvJi9XVF4qOYqsr5rIFmxOiZx5w818bsuC5a8fgBW\nfmlmnA9xL2ZkR39Cg0kngW9WlvUdtXRKOaKjzi7NeiUs2XvTS/Gqmyxrs/jIaicX\nTVkfm/UNks8c4Wi93RWDm06SVNm4JRhfZbE84PjE3fEJE4H3Eh3rS0V9NX3fzQa8\n/Q7vCi0L4motLiGFr/GhMietcQwkMLa0hV3QoSdbSrxHdv45LJgntXpoXFA+YIoU\nfQIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEUCIQDaKE1i8YTc5Fe/vmck8k/6q3hC...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending enrollment request to server...
  Server response status: 200
  Server response: {'message': 'Device iphone_3 enrolled', 'status': 'success'}

Generating key material for iphone_4...
  Generating key shares...
  ✓ EC key share generated for signing
  ✓ RSA key generated for encryption
  EC Public share: -----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEwcOdffPCT9EoNHtaQtC1QsM03Qm0FhPa
S9+fm/siC7Uf8Z/Lt6/a8CdLCGACRXnZVhXlGPrhFw9GGlyfHBntbQ==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4fOSdnXaT6GLEwKFCqA5
kkAGhvRZpPn0TsoMIeHykjaJ9roK3nZjhuks6z7l7CAnkvINS2LzdVovASwbDLmi
GLJu7O2+w0uE/j+nPnrr+rlnnuD1YYTXo+vW+B0YqV5GyRG/eM3kQJQjp10oII55
tVsSWzvoFBaOr8b5fC4+90l6F1SdMLVIZ9X8kDm+m0l3k8mizzCP1jRGOfTaTXnc
oNKm06wKqxpgMLdY0fZRsSBDwA6Sp8EsPcmECzbl4E9501O0MGLwu1lYjrHEctzY
ZMV9xf6l0NscbXEM1Or7nVkYcbnTayz2otTfjPBlbXykImSDZ7+tbrBHp9L20Gyr
jwIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_4...
  Data to sign: {"device_id": "iphone_4", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEwcOdffPCT9EoNHtaQtC1QsM03Qm0FhPa\nS9+fm/siC7Uf8Z/Lt6/a8CdLCGACRXnZVhXlGPrhFw9GGlyfHBntbQ==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA4fOSdnXaT6GLEwKFCqA5\nkkAGhvRZpPn0TsoMIeHykjaJ9roK3nZjhuks6z7l7CAnkvINS2LzdVovASwbDLmi\nGLJu7O2+w0uE/j+nPnrr+rlnnuD1YYTXo+vW+B0YqV5GyRG/eM3kQJQjp10oII55\ntVsSWzvoFBaOr8b5fC4+90l6F1SdMLVIZ9X8kDm+m0l3k8mizzCP1jRGOfTaTXnc\noNKm06wKqxpgMLdY0fZRsSBDwA6Sp8EsPcmECzbl4E9501O0MGLwu1lYjrHEctzY\nZMV9xf6l0NscbXEM1Or7nVkYcbnTayz2otTfjPBlbXykImSDZ7+tbrBHp9L20Gyr\njwIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEYCIQDQNWH9vPbanpyOkH3lrv8SuTdj...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending enrollment request to server...
  Server response status: 200
  Server response: {'message': 'Device iphone_4 enrolled', 'status': 'success'}

Generating key material for iphone_5...
  Generating key shares...
  ✓ EC key share generated for signing
  ✓ RSA key generated for encryption
  EC Public share: -----BEGIN PUBLIC KEY-----
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEX6cZVjRCU91/2Kmzfxp493GFHCPpF9Hh
Rzhs00iL+kmQwTl0ca9JI9lmBXEXeK7UyeuxnMHLuLjcERLRuJGOew==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAttiB4u7ik8C7835GUUtb
rBMRen+xI0RI/vuIVFuWh9jQLZ5KztUDjJkPmNgx5f4CamycFiCd7NwBu6X1SvbV
lzw5BMwOQ6wfiC95ozzKfqswCwVemAF2BDMuyl/8E4pMumL5T/ywPkCtL4gBHssx
aFlbkXJxdRoDcwlZ+ssSh7FpzeYWk/rR48o0xG/UbN2WiAHkSLQSSe6ipYXWzTMB
dAH99Q2/3Q/GY/rYMiJlqcOjCCcRzqcshgV0IJEUIOj5+M34MLNdyycwxD7F/PvE
QW7Vf6mHDYjREHzY7f/v8vD5D15RPn2ZAP6fY8XT4Jr963ImUFarQnJ8ilF/NJ9O
XQIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_5...
  Data to sign: {"device_id": "iphone_5", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEX6cZVjRCU91/2Kmzfxp493GFHCPpF9Hh\nRzhs00iL+kmQwTl0ca9JI9lmBXEXeK7UyeuxnMHLuLjcERLRuJGOew==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAttiB4u7ik8C7835GUUtb\nrBMRen+xI0RI/vuIVFuWh9jQLZ5KztUDjJkPmNgx5f4CamycFiCd7NwBu6X1SvbV\nlzw5BMwOQ6wfiC95ozzKfqswCwVemAF2BDMuyl/8E4pMumL5T/ywPkCtL4gBHssx\naFlbkXJxdRoDcwlZ+ssSh7FpzeYWk/rR48o0xG/UbN2WiAHkSLQSSe6ipYXWzTMB\ndAH99Q2/3Q/GY/rYMiJlqcOjCCcRzqcshgV0IJEUIOj5+M34MLNdyycwxD7F/PvE\nQW7Vf6mHDYjREHzY7f/v8vD5D15RPn2ZAP6fY8XT4Jr963ImUFarQnJ8ilF/NJ9O\nXQIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEUCICdT8YOAe+LSLlqpF58L6Yiwdv0E...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending enrollment request to server...
  Server response status: 200
  Server response: {'message': 'Device iphone_5 enrolled', 'status': 'success'}

=== Distributing Encrypted Shares ===

Processing shares from iphone_1...
  Encrypting share for iphone_2...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_2
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_3...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_3
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_4...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_4
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_5...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_5
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes

Processing shares from iphone_2...
  Encrypting share for iphone_1...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_1
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_3...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_3
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_4...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_4
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_5...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_5
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes

Processing shares from iphone_3...
  Encrypting share for iphone_1...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_1
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_2...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_2
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_4...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_4
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_5...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_5
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes

Processing shares from iphone_4...
  Encrypting share for iphone_1...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_1
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_2...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_2
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_3...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_3
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_5...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_5
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes

Processing shares from iphone_5...
  Encrypting share for iphone_1...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_1
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_2...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_2
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_3...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_3
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes
  Encrypting share for iphone_4...
  Encrypting share for peer...
  ✓ Share encrypted
  ✓ Share encrypted for iphone_4
    Encrypted share size: 64 bytes
    Encrypted key size: 344 bytes

=== Distributing Shares to Server ===

Sending iphone_1's encrypted shares...
  Signing data for iphone_1...
  Data to sign: {"device_id": "iphone_1", "shares": {"iphone_2": {"encrypted_share": "pZ50E1giEULIGUmf1AjXO+CEyEWedrdEDlws2IzqPXXOR6gMw/1tN4+GvQbZ6C0s", "encrypted_key": "Ze9l459/p/6FmFu17/XAawsAkRjPdppuc4joZrKXLhropyVPCDXd80UEuCNhTW+xAEzBW5jCnm5hEzMN09e80D5yINY314Z7VExwQfASxW/Y6Z9TNjjFpW5FlfzKwTH6jfVHeQNgkYdakaVaJxmoUVn/Z+hOjk3rgeRiMO4oYNAye7KX+lZJdaMAh/+FWYapaPS3lQS+qsQZKddrtEDEfKVumzaFjVrFiqwytUJm00dxCBmTtTjAKsq6g57/dYoAPAUDKXEFb/rPmwDK5JIBMbWguBtAt6JmMTUl9KhL3fq2sgtw/SS8F+CxH2SgcYU5zXZOXZt8f4pD0I1lULEQQA==", "iv": "2dzhtiqDBVMDyF5PixJUhw=="}, "iphone_3": {"encrypted_share": "jAoM9h97RHlvazdX4VVANOOK0rYS0bsML5KZyk93hYSS2JdRTVftD1ecnr5AZEMY", "encrypted_key": "anWFGUw1Hv0Tcf4RpZR1M3quQUjlFba6pvHQWVEgxum3qA3vlnMXLd5mTfePgC63vDjK/Sn6X9HvnEfR4fB484jhuwA5LoxZHt+s4LF/Z+OaHIUt1V1CCmTPane/sw/7eE1d098lqRkxsM6qvy6g9jYJB7HWmVdH6yMa1gpK2e1o9DySl0K4sKSCxuSUt1EJpZgdTPrinmkEON7jsQQ1+cyaa71WRI7AvjCG4vf+AN3LwLQFYx9u4NygoV3NNM4sLecqexaKOH2x2taNyV0MYQdO1bqtJHP9Z/SlnneK7gdwi4AKx5w3EBCOd45HJJyrA71QOk9dQxQyuwWDwSvoFQ==", "iv": "mOXg8fQZcM9eS0D9xbu79A=="}, "iphone_4": {"encrypted_share": "EGf/h8A/frmv3Lz5A1IGylO9I2lsK3QEd2adbbmPMgwpTZgDBUzIApP7ti8A5a4Q", "encrypted_key": "yQCPSdVi2FHQd6tk9FNbXw8ODXQwAJxwPvZ5awxahxAUuvflQI0xgp1t8J8xZDE9NPI8A/phOVglbQYjVjFT5HgA/V194dGdbmYBPtEgzXmsd8APKLP8Wv9RnK8PYtheVs/7csi4pYxj7tH9QxfP2C7nOras9jsmrU4kG6RQw8IjaIgi8Bjv2SEcO7c3rsg6RvG7YJGWVNVcvyFwc/mwtwAM70LvqQD+skQ5rzHG9NUIx7++WoI1WM5oRYkS4uGQObTTDZNsQAYeyeHsLFZYnEiMEdd5eDDVRrty4T5mVghWMA2dbZKOuFiIEC+62figVPlRkP3BfbPdL87Hdk9X4g==", "iv": "q0h5t7YFVMlEUhzkvcyR7A=="}, "iphone_5": {"encrypted_share": "A2B5cZiAsLpcsNLtWqOBCZlqM16wqahMda8N9GKZRiNxgjkLz5Q3NB7oMSFSXjrm", "encrypted_key": "PiDH1/QTRL8NYMg1YR+RFs+1moEmfl5MVQP2DxPfzcgyBiTBXXqkh66kMbn3CTY8eWw5Ujnw4vJfMGquQJhk/G9J9lyy9imSQOFsu77ULKPXnXjNRgB75hgvQrTCFYkgAUU8sP8CbILjy341wK6nZX0gLTwNqWrmhl1bqbDZx7wGfEacU5zdwg1+GcaWa4eeSOxAC980X2Zh+w/u7D/LsQTOkw1gzPGi/T7TmzQM79ef9767MPmpIR/mwVz1XAmf8/9Aj8qHePoVYA2EhCmhvcsGELbdIdTj59el9s0AkkwT8Aqe3JYPKqk+WacKCWU+zoJld0qUkLxgFcNhiWqxiQ==", "iv": "wkLFU+CMhfH7FmDmYW71dA=="}}}
  ✓ Signature generated: MEUCIEVa2qvmDYz+K7j+LdKmbrmdwymU...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Server response status: 200
  Server response: {'message': 'Shares from iphone_1 stored', 'shares_count': 4, 'status': 'success'}

Sending iphone_2's encrypted shares...
  Signing data for iphone_2...
  Data to sign: {"device_id": "iphone_2", "shares": {"iphone_1": {"encrypted_share": "mescwC9h8hRnl6mzCB2UY/DBLyGEkpOSKhfrGEo3igIZdkSnkpI5tvQGcd/9SzmH", "encrypted_key": "SlJ+DT7h/RFL49MG1DwyZmcFDsJirNGTF05bmiNNxwusgzfpXs+rB3fPtT6pJ++NUl1BU6Udx8pBqXiX1q45ypToSNJQcGhjHgEdgXA4tMyyu4tq/coVN6eATPcMDrZ+qPGrg/SG6qOOFm9bmrJAKA6zNUfwtXA+y/3Hz+QY+IT8/GYSXpJ1MmD0/E1uuCaZJy4QQU3yM6nWFwowPNNUKPuHwwYXOvcoMTRxzVuhAG4IsQQbIfa+6Zf7+M37+oTWwhagQA49zYhot5kTdqsf90B3Jh3wYRJWNy95uqfB68egzjNHiZDDwGKxYx1pciKFTx5a4BEojca+gcLlj7Qy5g==", "iv": "a1V8CkDN7rEOadxOsEk9oQ=="}, "iphone_3": {"encrypted_share": "Cpasnr4Tbb4zL+JR/hEBWXW7WKc7f5FbhPXsnSxT97zsP/TKMb69G3F2i5ea/r1n", "encrypted_key": "bGfa/fVXv2Gqw1ipe19WMQK0ZXZ0pysQ4FMYC3UquehQOtvErVEtcSKpgZf7EkIZpUXQvkOC5JjFC0JOnDkMOLNghTftmHq7QSToIHQ9+XoMaifeJlLwe/kN4+L6E6/e3AFUWYCnTPlMNsuEqZEUAMkjqoVdfdAei4fGWCJaAHHOobLioipULh6wrSx5jxc6rSoanqKnJDFnTqTivmlYJlthMbASOWfcDAmF3r2g7bYFwOcX3YLo+p/PkJK+k0+fpnEDfjjU/Yuj2XTek7w9W3Pt/EvNrhfantZwidc52YDlctiWJ/WFb7AjTpbptTdOYoggW5sVg0T4BNBiqXP+/Q==", "iv": "M2z7CCp4bT60ZyM90IldWA=="}, "iphone_4": {"encrypted_share": "pvcFPfboiGxpmDJN2+KEIcjW68DixxUQwK23ngdJYdw0EHAlwMaWLw7SiFsHmOqE", "encrypted_key": "2xANSa05SdtP4tRJR6+S7P/m2klQQPCeUyNOjX1CaCVNHCjaIb9/VxupQihFD26DnE9yRcQ0vXtkn0bhU5n6DdDLBlz8n8eALuikEH/3oYskVIkDuRLcNHnfZWK0VzqqY31vge7P2t9BWSiE+WwOIGgq2w+ucePCFUHbKGjtvafdgTyLR825m9IEeiGbcVWaLdMG+6F85FCxjbXpnqkiw/bPL0+F59tSGSTjrs58hnNITT/y4oW2F0gpkZW3jatdb02DM/hHETWTCDS4IFrksZrs2WvaOh15t7BQgaoeQ+kdvHZIYLRpJQ5u4OWt1B0UMT9TLdgDGwipjZaZSn5CIg==", "iv": "lAzJfd8cWn3ToJtRbJcOuw=="}, "iphone_5": {"encrypted_share": "aNWfbDx0n/o3A/DfvnYCioPYOk7EwgiAK4iNsgkVDeMZczja1Ncj8zvr3G4A6p/v", "encrypted_key": "owcgZcVtBhpEFr36ldPWoqhPzWEqVK6hD6ERbwJS1dHl3iCCGZNo1ZJ09PEK77kJABrxR9RyUYvo+NNWUwhohHBq5TaaQ8F9x6mZWKQ/Iz2R1Fxb5lTbb3fAzWgC5bYdxSrM5PYUGwtyVXjr6pyBxk8eLGf8JXg2TlQyotJaxeY3LrS1e6NT8+maTz9i5I9OMzpGG6adLxDM9BeAAHvdhMGmVtVHo+yzJ8euedVqDV8nZHJ2n7hCpBdkL6xA3yNby2RUKr6lnEknTalTTk+LszF2eb2eZ26pU8fQEsOmOr849Zp2j3zQA0GhRrF498OdRsP3wzhu8nnBAgGCPFHPKg==", "iv": "Tj6ho3B+5n3fc9aAyU8c8w=="}}}
  ✓ Signature generated: MEUCIQCEUFgi1RMGWoKQCNIdg1Ug6fFi...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Server response status: 200
  Server response: {'message': 'Shares from iphone_2 stored', 'shares_count': 4, 'status': 'success'}

Sending iphone_3's encrypted shares...
  Signing data for iphone_3...
  Data to sign: {"device_id": "iphone_3", "shares": {"iphone_1": {"encrypted_share": "brRALX42yqPqNmL2EgKfjNKKW1j1YWTdyKzu/puRF/xk/1V1b0X2Lg+04R6M3NKL", "encrypted_key": "OVyvWga/AcWa6iVQpML8SaieVrNrsqvvjcQ09cJUiwg8xo3crh6m2EIi9cSY5tN1imu5+8H9DGwvPxV8zqBXZZJSIvv9gHUcxZfQg2pR2kzir9mAwrbL6NM0ig2BWxsfig+uF1W6LdsIv6+OrE/rc+vS7nUVK8d229pGBG0Oq9EiJZjb+g2erPM0woFV+hjYjGzK9nIza2btRsLXPA7y2YCdfrjMtOGE4TiJnXazyEBjGXDP+VpAjAHrZ5pJLd8AbjFX2SLo6Z/Uaq2X/DlDWm+9u1BNv+34qd98vtpRwpEhM8THcKA4L6zXNLGqILRBsRtXuahOQMo1hpdCub+jNw==", "iv": "Ad04JOmbDNdIJnTeobXa1Q=="}, "iphone_2": {"encrypted_share": "d6mZmNj5aRO6FYXNzCz5BGTRykvs5uTDnyvy6HRL8Nam97jwU8mPr3hQKL0C3djS", "encrypted_key": "OfS2L3d0rJMU2OMvUco54uqS4REF/1ImYxLE2OrhAEKPa6WJZZ2MUyON/OrWGyJa+ohjmb5WCCGpLpjmxRKIzrT6laco4SM6DNMnE6q/vtugEjeq2ftVZEakKT9ce6eZKiqzJwkR/n2nTVpbkF3URIq6iMjL5c50ag48DrWL2umAvYzdYOuuJ20VXa5MOYmqnGX+Kk8Q2gxx0ygk3MvNH9bW6PURuqJoXpJ/wqQ5E6ha/JoKd5EpfNa/YpqBD1wudMYpafHPoWun5YWkowiik7btqWIf2umpWTATFZml6A/YjoxiMKSuLp3l+aEKOGFe8OKf4T3DtkgnLIrJjhB7BQ==", "iv": "snh3Tokw5SVfadluuFqwPw=="}, "iphone_4": {"encrypted_share": "3QC+4rvPFokhffU55RzJD3mcy+6H1HSZjAD6p5USs/v7/Om5zoAePhQrVEScQc0h", "encrypted_key": "1cyVCfsI+ZW9HoJSvqKrPvvjLWsjqyANI33QpdfTRWEZPmd2VYqf58QuY516QYkF2Rdn4trs+josfLn5cp8Zg8EplpDPsTTrn6FbKHaHH4LDAVTrLoSxn4RkF4WS/ffGgy3TUFd+q5lfxFsiFFvVNZ+zl3nbLeOxyRaAq4Iti630YnXQSDd+596tIPEkGYn/EVn8zmsMGHapjYW12I0xa9Odsesbr7FBwPaW4kX9i1mz6dXGOazaYjBtlIHWIBUAm4liy9pooy45FSXu5Fi3AZ5nJfwevrjYpEtlaSwsNeA1Yd3Zr9CMKDa/iJjK4Eq1NiQyWLEsny1HaQj1cqPUWw==", "iv": "x0QspLD2P2HfFseKnaLf6g=="}, "iphone_5": {"encrypted_share": "1EAe9DHf4j//mMlxQ0TM6xkScqj6l95x2MuRsIf9HtPM+hFw0VGSfidpbsp/j7p7", "encrypted_key": "PXAHOqihSvIS6DDd3roaOhv/vJr05qTouC+KZ5KrnPCn+Zg4PQlI9tiIa+ryXk/j0h3f2g1vtA33HrZinYLH/vMQgaqPfKzhtFNALkF4Dmmu9vQY217HVgJuM1CRZ/TTdebdzOAB8pJn/+1KOo96He7xfX06XG+tSjeE7io44u9zZxQqfCZMog1fCz9JnXiQ61NMtrHzchIryEEDtN3hs+/9tihv3aQn5jhFCBMAC+/ufIGbFAB3oVRrlD5MJVciZUJ6lwJHUdCGZhWqj23lydq+8WniO8EdXhyVr84RrAeM6aqGTce3uii1nYP+zI+aJO3n8B/rITGo0qxZOCe6SA==", "iv": "gvuZp5dKLV0ZlWzLrzIhcw=="}}}
  ✓ Signature generated: MEQCIHnfjMqHkYmA0i0ZKwZhEwXsvbtn...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Server response status: 200
  Server response: {'message': 'Shares from iphone_3 stored', 'shares_count': 4, 'status': 'success'}

Sending iphone_4's encrypted shares...
  Signing data for iphone_4...
  Data to sign: {"device_id": "iphone_4", "shares": {"iphone_1": {"encrypted_share": "jdpLQ6bdyLNwcyovEVrmV99Hcv4PcplO8LeiXEKr3QP68+zv9QvRBbnfsr5D+6yH", "encrypted_key": "GxNek8JoWKOm83Ca+ibSn3O5tcTgbvURwJJPmV954V3FalGiAl6mm1+zWO4Lw/QH1rrpv17g57SOkehWZBaSfqkhBrSLV44Cq3pq0UOvVo4mCcfMaUYU1V7qsdbaR3Bwj0sPxDGK5nQiq4axrwiJ7mRFuNlafRizFpq9ZrCyODmzSSpWTILDWco1So2TVJBQEbCfSBO7LrjqJh70FZK7iY2RY9Pdf26D+ITgcRAPysMJbyzMe0KLWZblgxgK/nwe2aHFGnEOuufe5c5ckIoS0ZQCZeWX2KR46SlxQNlxqWGbv50GS11wEY4FnS050Vt9bGa2c9qwHIi8AjAl0vcTkA==", "iv": "mSL1ZDTMpUayLS9GaTuVgw=="}, "iphone_2": {"encrypted_share": "WWhsJTmcJqrvU/dyt0eO++qgxGjxH3GvEptEoy6r/IcWi18rK/qEkw742hlMtGGn", "encrypted_key": "VXNRjfrwAwla2yslwUvHxsb+KXKStzrLsIXDFb06wGWrvTwVh0cUUCsodRgSOxuN0TXdUqswx//46U4baIavaUZ+hUbDJN3XPfHuXnjTWmbecuM47cgltRkJey0rV79MAxIEyy3RSYI90MMgmNCV2UcMjspr0QqGDAbD5qaHPvCrwWeS8pUuGXEfmRWNLVt6umt8rsGKeNdCZCLLdFgJkSxIFfY63EJ3NHfLPDVosmH417u2V0EHunTlFqX2ezUwBncYkrdunkJ2b0CkrPgPZlG1dTuhVX6AVdKG9zYzwoRsA2TSVh9MUFm9wnQASaglnkwP0mkuw13QEjwxuv5yiQ==", "iv": "J7EWYxX51C9VgiA2gClsWQ=="}, "iphone_3": {"encrypted_share": "X5Z06mIaC9mQl7qVceejI/NEur3SsIqaed05CZMQrquIXsBDw24/4TyDmRLAmogf", "encrypted_key": "Q20aV5NWCcyyaZuxrMJSgxlmVt0Y30HyTNfgHnp/oDjbmr2QEJYzIeLLQo3Vp1YXZv8xegt1MO+zdvb2E721xMBYq/AWPCDpUwmVOsqqRFXMQdA1z7eb16841V7wdpAQEYzV1SNqkf1Svc8anhCC/MHeJP6t3KZDyPkoDm/p5n0nkMuFBgk4Kn+bTvXR9ScaAXY/sd3WMcVkgS9zBVaPbTCmYHNKBySC6BEgt0WaoXDmw0wI8CrZZsn3HkmZAZshHSWSILU9Ck1jy6fvROJOSAbh0Bd/3Kb2D6q0dX9Gfq4Dsw/Egkh5rnKVwirq2119BF85qVCB6y4klJm6V2wznQ==", "iv": "VOrya25W6XeFk1pN16RL4w=="}, "iphone_5": {"encrypted_share": "YidTJ0NBoT55Vx0F0jNJ3n5uRV0QR5GYLGPpuEXFFht+wuS1UAVRe9Q3fG5ghfBF", "encrypted_key": "niBtDqn47I8ESKfkJN2vFeOZNIVWetGBFfuNyofma5LeyZQDA5//ov9ynNly+U7D86pqMVofxoVL9K33s/MLxwSr45D5T3rqHMvmKZ0IFt6qkT69qjKXTtiugm5CTuAb8KW/xLVRwa2nD7kTd3q0U/cKMTTOlpvUVopMCDrSGFihlfoQp8NQWRtB6LH1c1PT1/yuWA96HOyg8vs1lQSMA9d7Gu9y8gnLo3gI5/b2hsPgIJOtLaE+38uzkEruREk5EaXJZrlRSBEfv8caZKwlRdfrFPHgv5TtkzdmbIP0sNcs2sRgl6V7xJkz8WCoLJUSIvY2u0vQg429KMrd7p3/KQ==", "iv": "sXOQMwKJ+T9Ypv3juLQNng=="}}}
  ✓ Signature generated: MEQCIHnkGyQxtPuYLfCQi2DlZYXHikYA...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Server response status: 200
  Server response: {'message': 'Shares from iphone_4 stored', 'shares_count': 4, 'status': 'success'}

Sending iphone_5's encrypted shares...
  Signing data for iphone_5...
  Data to sign: {"device_id": "iphone_5", "shares": {"iphone_1": {"encrypted_share": "dIWxVDAOm6u7awNmrxiqt7JFXgeOqnEzU9i8ImVPr4GjT7F2I9/eN/b+W1aulu+f", "encrypted_key": "PszSV0UXsRQyO9WCR1+GCTW/5Ztph5ABmblEbB5PzTNnnZRlKyPzUB0ehMGPA4IULfaUxsZqsF/YHLoSkDFt+FIVhUYiln43pzzMmElHDYDa2eAoBAXkNYbx7gw5JnMqeoHna/RejatqtIxJQN/qLvXea+kaR4ag5ttICIsTAX8xAdxz/QFD9bemRmYX+gQ1/B/rJm6gGk6YzpqHPcJ7IVWslOSrOkUvn9Nf4/51dHBHlxjsBQLrwr2rVxclRxHzHdB051YFIPXej/NGxMic5bp44iNrzT0fGRVhT7DBv8T3m6dClYRUP/aITI8MdH/f2aARSixsZ7TJTJenJj1WBg==", "iv": "ZfcdDR4FKZl2u3qewRUDEg=="}, "iphone_2": {"encrypted_share": "RabRAz92h6fg669KlSQ3TKjuej/xQ7hpuNja7KKrQGwM6GXOSw0yS7dUHpKx2PQW", "encrypted_key": "gqkFLgjWsz12WnQ/5LEGHDipQTEjm47uvtMEi9ZVi8epRSy8OjS3zSKEcXzeNrXEyhb+PE1R7HLV98FlgQG3whBzaq1vzz9UpSa91iJoQmQ5xqFFz5N546nQIFexS8Bvl3MyWid6gHbZeaJxVA0y8Js5Dkez6y61t3QruAv6Km+w/sQHlh/Z4T6k33k3GOSjNyAgk+4p0wxo0nEWBmWpKST9F+F5N7XN03StRQnrdFxp++4/dXlSMYJP0/GBq6Ujq7L6PrwMm4HHD8GdTgkdPtgR6LL6kf6rlcmCdpaYofaHKMXj7/CyzLb9Ii7/U1meBIgSFIzY+SBUnTTPeqPq2w==", "iv": "sQU2jaXasTXVnuTYM7UAJQ=="}, "iphone_3": {"encrypted_share": "5RpldGOvuHmWn8fgQAkUi9bEvn3pbc3hau02teWphPdavdbXfJ6Y4d+YaMk7XFuP", "encrypted_key": "gyjnjuDTsNIsfEBYqnRVrZhsBd9Q0nJOu8BwGPw5QWYeDfJDhM4dcBDCQ8WN17T6JCkIHpPrJRS5sf/nm2h3M4E3XVNGS4iKrtVOZ8m15APfLCZnId3ww3UuEaKHDsHzZ7dCvJ7RW/jj+CfmA/bB2JUyXeQ5WSoc2J8rkkZxWeMgaWhbDU9AwPU7XF8ZMxfPGMcYcbyy+kB5VrTk7JUfP7Nz1PZ/gXOz2q5brJj04oJHStwYqAnJJ9qFiOzIlxnzMxv0mChl+nivSiOtNJA08h87v3sPeA0Z09SrcdKNVrlBXtc/8EA3aURuLK9Q7St6YN5gxkJPH1oYhTn6AWTS5Q==", "iv": "VeCzVsZpBY6jw2XbhY16HA=="}, "iphone_4": {"encrypted_share": "P6O/UVfFFp+j57LQ3x8FZCGdU1v1X8dWDh1tdDxdfH1pwbdsTuBbJeeYQSJnRNJz", "encrypted_key": "F3gDGHsGhHvmt0f/HmUaxsEvHhdrXGlbkLne410/SupS5NV9KWFRq0c7vyYu8sPPmPC5uqT03zw8upasjXNkKTFHqI1tqR+Ftcmx2mqx6WpQkbx3EOaqpXf3Zx2xUBKBq1jv6C/26L18bpAcE4Lm5qH56Qr4dxpKndb5yxLk4VfmJ415S2jjdhOdJDqwecWR6mjblPvywU9FE8/4Pt/JS3JUxZ3Ik/9plnLiK4VjPsVuOFHs+vZ1jYBDQ2usvyeVyCSEI8kEWmkyc4Yd1Wlj47vCdEkp9izhQEGcCxT+Go+56UEvzJhpLyz2y1AfNLOO8NpHUlo9s8e5XrDBg41MnA==", "iv": "5Rc0zrHf4bMWkcNBKBPraw=="}}}
  ✓ Signature generated: MEQCIBFAnZ469lg111ULWsQ1noWun+rp...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Server response status: 200
  Server response: {'message': 'Shares from iphone_5 stored', 'shares_count': 4, 'status': 'success'}

✓ MPC Setup Complete
  • 5 devices enrolled
  • 5 sets of encrypted shares distributed
  • Threshold requirement: 3 signatures

=== Requesting Transaction Signature ===
Transaction data: {'to': '0x742d35Cc6634C0532925a3b844Bc454e4438f44e', 'value': '1000000000000000000'}
Server response: {'message': 'Transaction signature requested', 'txn_hash': 'c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160'}

=== Submitting Partial Signatures ===
Transaction hash: c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160

Fetching aggregated public key...
Threshold wallet address: 0xf13a446b6bdeb8ab5c07f4b0aadbe979caab7c1d

=== Collecting Partial Signatures ===
Need 3 signatures for threshold...

Device 1 of 3: iphone_1
  Signing data for iphone_1...
  Data to sign: c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160
  ✓ Signature generated: MEYCIQCCTBqNfv6coa5MUKh/PoyIh5C6...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Partial signature: MEYCIQCCTBqNfv6coa5MUKh/PoyIh5C6...
  Length: 96 characters
  Raw bytes: 72 bytes
  Signing data for iphone_1...
  Data to sign: {"device_id": "iphone_1", "partial_signature": "MEYCIQCCTBqNfv6coa5MUKh/PoyIh5C6hjWIvE+CMFhsrVLT7gIhAKr1qvWLPzHMSigElS/r6W2lpzbf4S0vKQflf1y3mask"}
  ✓ Signature generated: MEQCIHCPc+OTlP6pmoEgf9eDyWXB+X1T...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending to server for aggregation...
  Server response: {'final_signature': 'MEYCIQCCTBqNfv6coa5MUKh/PoyIh5C6hjWIvE+CMFhsrVLT7gIhAKr1qvWLPzHMSigElS/r6W2lpzbf4S0vKQflf1y3maskMEUCIQCVqQK+HA++7uy6ftlZPVCc1KzmxDDLANFx0ICZVcL9tQIgGQLf8PZ0SDWfyx4AeHDVLBQAPPKrxMzDeU80NwLInts=MEUCIAX+Xc+yLMvyvIkYWZkofbdq7brC0KmGxzP2rdOTe+pwAiEA9rf17xmLqdTGOqmX9vor/HT8sznBnYkcn4/UuDqp3zI=', 'signature_ready': True}
  ✓ Threshold reached! Final signature ready

Device 2 of 3: iphone_2
  Signing data for iphone_2...
  Data to sign: c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160
  ✓ Signature generated: MEYCIQDSoKIlnrNOsfkgA4ZpqEDAmtUx...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Partial signature: MEYCIQDSoKIlnrNOsfkgA4ZpqEDAmtUx...
  Length: 96 characters
  Raw bytes: 72 bytes
  Signing data for iphone_2...
  Data to sign: {"device_id": "iphone_2", "partial_signature": "MEYCIQDSoKIlnrNOsfkgA4ZpqEDAmtUxZ6sD7bwtFoWFgJE8CAIhAPT+kZ5zw94vM/Aa3Nq6TI69FujXe0BKSDS7LWCXDnsl"}
  ✓ Signature generated: MEYCIQDx4btapaJhyMlmCEKHwyu91ned...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending to server for aggregation...
  Server response: {'final_signature': 'MEYCIQCCTBqNfv6coa5MUKh/PoyIh5C6hjWIvE+CMFhsrVLT7gIhAKr1qvWLPzHMSigElS/r6W2lpzbf4S0vKQflf1y3maskMEYCIQDSoKIlnrNOsfkgA4ZpqEDAmtUxZ6sD7bwtFoWFgJE8CAIhAPT+kZ5zw94vM/Aa3Nq6TI69FujXe0BKSDS7LWCXDnslMEUCIAX+Xc+yLMvyvIkYWZkofbdq7brC0KmGxzP2rdOTe+pwAiEA9rf17xmLqdTGOqmX9vor/HT8sznBnYkcn4/UuDqp3zI=', 'signature_ready': True}
  ✓ Threshold reached! Final signature ready

Device 3 of 3: iphone_3
  Signing data for iphone_3...
  Data to sign: c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160
  ✓ Signature generated: MEYCIQDFOHg+D6CTQNxMXgylGMe2NaoT...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Partial signature: MEYCIQDFOHg+D6CTQNxMXgylGMe2NaoT...
  Length: 96 characters
  Raw bytes: 72 bytes
  Signing data for iphone_3...
  Data to sign: {"device_id": "iphone_3", "partial_signature": "MEYCIQDFOHg+D6CTQNxMXgylGMe2NaoTV4nfLRggxh3x2vMYEQIhAIsImElYFXX+yEAnWqc2OWAnOTsxqbVrnrh5UpVKZ94+"}
  ✓ Signature generated: MEYCIQCbUJ5Bf2AoSupJUksfcCPyIuyP...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending to server for aggregation...
  Server response: {'final_signature': 'MEYCIQCCTBqNfv6coa5MUKh/PoyIh5C6hjWIvE+CMFhsrVLT7gIhAKr1qvWLPzHMSigElS/r6W2lpzbf4S0vKQflf1y3maskMEYCIQDSoKIlnrNOsfkgA4ZpqEDAmtUxZ6sD7bwtFoWFgJE8CAIhAPT+kZ5zw94vM/Aa3Nq6TI69FujXe0BKSDS7LWCXDnslMEYCIQDFOHg+D6CTQNxMXgylGMe2NaoTV4nfLRggxh3x2vMYEQIhAIsImElYFXX+yEAnWqc2OWAnOTsxqbVrnrh5UpVKZ94+', 'signature_ready': True}
  ✓ Threshold reached! Final signature ready

=== Signature Aggregation Process ===
Partial signatures collected:
  iphone_1: MEYCIQCCTBqNfv6coa5MUKh/PoyIh5C6hjWIvE+CMFhsrVLT7gIhAKr1qvWLPzHMSigElS/r6W2lpzbf4S0vKQflf1y3mask
    Length: 96 characters
    Raw bytes: 72 bytes
    Raw hex: 3046022100824c1a8d7efe9ca1ae4c50a87f3e8c888790ba863588bc4f8230586cad52d3ee022100aaf5aaf58b3f31cc4a2804952febe96da5a736dfe12d2f2907e57f5cb799ab24
  ✓ Signature verified successfully
    Verifies: True
  iphone_2: MEYCIQDSoKIlnrNOsfkgA4ZpqEDAmtUxZ6sD7bwtFoWFgJE8CAIhAPT+kZ5zw94vM/Aa3Nq6TI69FujXe0BKSDS7LWCXDnsl
    Length: 96 characters
    Raw bytes: 72 bytes
    Raw hex: 3046022100d2a0a2259eb34eb1f920038669a840c09ad53167ab03edbc2d16858580913c08022100f4fe919e73c3de2f33f01adcdaba4c8ebd16e8d77b404a4834bb2d60970e7b25
  ✓ Signature verified successfully
    Verifies: True
  iphone_3: MEYCIQDFOHg+D6CTQNxMXgylGMe2NaoTV4nfLRggxh3x2vMYEQIhAIsImElYFXX+yEAnWqc2OWAnOTsxqbVrnrh5UpVKZ94+
    Length: 96 characters
    Raw bytes: 72 bytes
    Raw hex: 3046022100c538783e0fa09340dc4c5e0ca518c7b635aa135789df2d1820c61df1daf318110221008b089849581575fec840275aa736396027393b31a9b56b9eb87952954a67de3e
  ✓ Signature verified successfully
    Verifies: True

Aggregated signature: MEYCIQCCTBqNfv6coa5MUKh/PoyIh5C6hjWIvE+CMFhsrVLT7gIhAKr1qvWLPzHMSigElS/r6W2lpzbf4S0vKQflf1y3maskMEYCIQDSoKIlnrNOsfkgA4ZpqEDAmtUxZ6sD7bwtFoWFgJE8CAIhAPT+kZ5zw94vM/Aa3Nq6TI69FujXe0BKSDS7LWCXDnslMEYCIQDFOHg+D6CTQNxMXgylGMe2NaoTV4nfLRggxh3x2vMYEQIhAIsImElYFXX+yEAnWqc2OWAnOTsxqbVrnrh5UpVKZ94+
  Length: 288 characters
  Raw bytes: 216 bytes
  Raw hex: 3046022100824c1a8d7efe9ca1ae4c50a87f3e8c888790ba863588bc4f8230586cad52d3ee022100aaf5aaf58b3f31cc4a2804952febe96da5a736dfe12d2f2907e57f5cb799ab243046022100d2a0a2259eb34eb1f920038669a840c09ad53167ab03edbc2d16858580913c08022100f4fe919e73c3de2f33f01adcdaba4c8ebd16e8d77b404a4834bb2d60970e7b253046022100c538783e0fa09340dc4c5e0ca518c7b635aa135789df2d1820c61df1daf318110221008b089849581575fec840275aa736396027393b31a9b56b9eb87952954a67de3e

=== Complete Ethereum Transaction ===
{
  "raw": {
    "to": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "value": "0x0de0b6b3a7640000",
    "from": "0xf13a446b6bdeb8ab5c07f4b0aadbe979caab7c1d",
    "nonce": "0x0",
    "gasPrice": "0x04a817c800",
    "gasLimit": "0x5208",
    "chainId": 1,
    "data": "0x",
    "type": "0x0"
  },
  "signature": {
    "r": "0x00824c1a8d7efe9ca1ae4c50a87f3e8c888790ba863588bc4f8230586cad52d3",
    "s": "0x2100aaf5aaf58b3f31cc4a2804952febe96da5a736dfe12d2f2907e57f5cb799",
    "v": "0x1b"
  },
  "hash": "c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160",
  "from": "0xf13a446b6bdeb8ab5c07f4b0aadbe979caab7c1d",
  "serialized": "0xc5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab16000824c1a8d7efe9ca1ae4c50a87f3e8c888790ba863588bc4f8230586cad52d32100aaf5aaf58b3f31cc4a2804952febe96da5a736dfe12d2f2907e57f5cb7991b"
}

=== Transaction Components ===
1. From Address: 0xf13a446b6bdeb8ab5c07f4b0aadbe979caab7c1d
2. To Address: 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
3. Value: 1000000000000000000 wei
4. Gas Price: 20000000000 wei
5. Gas Limit: 21000
6. Nonce: 0
7. Chain ID: 1

8. Signature Components:
   R: 0x00824c1a8d7efe9ca1ae4c50a87f3e8c888790ba863588bc4f8230586cad52d3
   S: 0x2100aaf5aaf58b3f31cc4a2804952febe96da5a736dfe12d2f2907e57f5cb799
   V: 27

9. Transaction Hash: c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160

10. Full Serialized Transaction:
0xc5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab16000824c1a8d7efe9ca1ae4c50a87f3e8c888790ba863588bc4f8230586cad52d32100aaf5aaf58b3f31cc4a2804952febe96da5a736dfe12d2f2907e57f5cb7991b

=== Final Status ===
✓ Transaction is valid and ready for broadcast
✓ Signing address verified: 0xf13a446b6bdeb8ab5c07f4b0aadbe979caab7c1d

✨ Test flow complete!
(thresh_venv) cmc@cmc-pro thresh_demo % 
