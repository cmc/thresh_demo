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
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBnzw07+ueb519IiSEafz1ZuYKDM77kX2
n+FWaBooGAaSj77LR4nOAqyyVtCIXZYPhOGdPgrP3C8nQ/4Ek9Chnw==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqwnygVJNjP4gmXrAYz78
IMUxcqjnsNsX4D3aYWc4M/xFxqr03SLEX97389RNi92LXeEzRRcKvh07OJhAFNox
9wT0ZsxZAz8+Jsde1NCuYPb/zO+y/Wy3UZ7c3kzywnFZrlK2wIUuYQDc2jQgoNlH
Vl4Kg9dTN3739a7rzqzdAfedrHWBxhxzwis9xGhYlC3oROK6KIZQ1VrJaAfXDtYU
IOqS3844ElAKn5zfVCTbe5KF/zj8G13EbAm5oH4A2/fYl9zOoKkXH6OIXqhlpcpU
Aa+pB4gvgOiWBt+5nw4ytx5PgfeVA9fRg45NM0fai9NKez1/zVMB/lLaNwHDwffC
gQIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_1...
  Data to sign: {"device_id": "iphone_1", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEBnzw07+ueb519IiSEafz1ZuYKDM77kX2\nn+FWaBooGAaSj77LR4nOAqyyVtCIXZYPhOGdPgrP3C8nQ/4Ek9Chnw==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAqwnygVJNjP4gmXrAYz78\nIMUxcqjnsNsX4D3aYWc4M/xFxqr03SLEX97389RNi92LXeEzRRcKvh07OJhAFNox\n9wT0ZsxZAz8+Jsde1NCuYPb/zO+y/Wy3UZ7c3kzywnFZrlK2wIUuYQDc2jQgoNlH\nVl4Kg9dTN3739a7rzqzdAfedrHWBxhxzwis9xGhYlC3oROK6KIZQ1VrJaAfXDtYU\nIOqS3844ElAKn5zfVCTbe5KF/zj8G13EbAm5oH4A2/fYl9zOoKkXH6OIXqhlpcpU\nAa+pB4gvgOiWBt+5nw4ytx5PgfeVA9fRg45NM0fai9NKez1/zVMB/lLaNwHDwffC\ngQIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEYCIQDCQs4OMJIQ5VA3O9Y/lYk1TlFj...
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
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEOVELyO+6w5FQrljA5vtguXOH/7iem3JR
phWqmWb7efHnBgkQ3k27JkaXo9iLR3mOxqdk6mLmbRZK6TqldsDgIA==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArSFunC2yZDAOxJSdgk3g
TD3vr6WfRX4oseUej71OvLfH06OROekMZWuzVxD40eyG6atSAxIgqElrIgPLb+r7
xqJDPlx0S86npGtAJbnkSXKAde7PW7Zt9W+APXV/3PdbTA9glcvGD4WcMPIq77XA
rgAsiBoKz9AcYzAmBcuZueS55ldVcD1yuC88efgM2Qq4utt+T60nwgdX5Yc+tsET
uF0EPXE/in5XIHQXKWfS5h8OssYe2Gi/SOC6dBAdzndTza3UOfPY+tk5Gq8oQlO7
uEPOYs8XSkR73lcCGUPsm8QfSakXhFGzs+dDOxwXUoH05YOSwyVOOFuAqxLyb2M6
wQIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_2...
  Data to sign: {"device_id": "iphone_2", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEOVELyO+6w5FQrljA5vtguXOH/7iem3JR\nphWqmWb7efHnBgkQ3k27JkaXo9iLR3mOxqdk6mLmbRZK6TqldsDgIA==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEArSFunC2yZDAOxJSdgk3g\nTD3vr6WfRX4oseUej71OvLfH06OROekMZWuzVxD40eyG6atSAxIgqElrIgPLb+r7\nxqJDPlx0S86npGtAJbnkSXKAde7PW7Zt9W+APXV/3PdbTA9glcvGD4WcMPIq77XA\nrgAsiBoKz9AcYzAmBcuZueS55ldVcD1yuC88efgM2Qq4utt+T60nwgdX5Yc+tsET\nuF0EPXE/in5XIHQXKWfS5h8OssYe2Gi/SOC6dBAdzndTza3UOfPY+tk5Gq8oQlO7\nuEPOYs8XSkR73lcCGUPsm8QfSakXhFGzs+dDOxwXUoH05YOSwyVOOFuAqxLyb2M6\nwQIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEUCIQDf/rXokJNx6zENIy94Ucd5X+w0...
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
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE9WsrgnnM6DL8AQB/mKLD2Y3L+IRVNHoh
g5rDLRUpwpnhcxsZCN4BuHPvFApYt31BtvALqo0M2r6zbPO7JJbZeQ==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjB6lb8/CrfQkQCHNlpWO
bZMWSbTsG3rW/xRw/3SBxkSCA8UyQoGhZatvc+wKPl4B+L+kbwji2Qf0zlQo49V+
P4Ms9hig959Q0nPmN4SQow5PJsdoaX9peHGgmZNFqT3MHzLiRWTAAIuYT+NKPtGy
xUdpu4QCrbyIZzxDibiMMUfmAP4b4+Qwm55t0PUg3Leuzo9iCV9becl3uinh4hG8
wVWiv3HaMZXMRQHEmikcOA7Op+UrbYnYhq1OBOtTHBEbCRH/b2yoOSeQ5kQKFDA/
fmcyJkChh5U3U3/rR1WT1s8HzTfTjOcVLIbFyQy5dqpZYrFHJVgnxmXN6ijWSC2V
MQIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_3...
  Data to sign: {"device_id": "iphone_3", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAE9WsrgnnM6DL8AQB/mKLD2Y3L+IRVNHoh\ng5rDLRUpwpnhcxsZCN4BuHPvFApYt31BtvALqo0M2r6zbPO7JJbZeQ==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAjB6lb8/CrfQkQCHNlpWO\nbZMWSbTsG3rW/xRw/3SBxkSCA8UyQoGhZatvc+wKPl4B+L+kbwji2Qf0zlQo49V+\nP4Ms9hig959Q0nPmN4SQow5PJsdoaX9peHGgmZNFqT3MHzLiRWTAAIuYT+NKPtGy\nxUdpu4QCrbyIZzxDibiMMUfmAP4b4+Qwm55t0PUg3Leuzo9iCV9becl3uinh4hG8\nwVWiv3HaMZXMRQHEmikcOA7Op+UrbYnYhq1OBOtTHBEbCRH/b2yoOSeQ5kQKFDA/\nfmcyJkChh5U3U3/rR1WT1s8HzTfTjOcVLIbFyQy5dqpZYrFHJVgnxmXN6ijWSC2V\nMQIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEQCIDi7aSWAqaer1IrKoys6zlVJkBSZ...
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
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEFxSVP+NGCvgCbIzEKiFDNvx0s8abWZM4
Mk6XMck+8P9wR04PUK/LVX9pkatahGsdJr7g2rYzBMYCVM1NpUT0zw==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3M/pGOgLHGS9NwrGMYx1
MrlbsrSlcneH0LyoR/CB0sVe9PFbJlE+JkQVH93FiGRh4zOV++UyuWIIgSIl9v2L
QTGXILDWrmGQoaq0HmAp9wDDNysCI4e6b0frgMOBh3wgdeltFWHtRi/rdEOn3BKp
km4HHs0WzO505CPtjxYpafvKwzeDTSgYrTZgR+5dYC1KCC9YKamT/F+TUgZMmWHM
9r9Q5gJ5O+rzE2IzqlSurPWBFkN8QeUWWyNBmcULRk6JiobXEmKIyu0l+Fn1tdHN
JwAaXIFXdNu0NW8lAdF7HqtNiU3kUshqTvloggI8sjy2XJ276M4QXVf51B5xXnmM
bwIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_4...
  Data to sign: {"device_id": "iphone_4", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAEFxSVP+NGCvgCbIzEKiFDNvx0s8abWZM4\nMk6XMck+8P9wR04PUK/LVX9pkatahGsdJr7g2rYzBMYCVM1NpUT0zw==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3M/pGOgLHGS9NwrGMYx1\nMrlbsrSlcneH0LyoR/CB0sVe9PFbJlE+JkQVH93FiGRh4zOV++UyuWIIgSIl9v2L\nQTGXILDWrmGQoaq0HmAp9wDDNysCI4e6b0frgMOBh3wgdeltFWHtRi/rdEOn3BKp\nkm4HHs0WzO505CPtjxYpafvKwzeDTSgYrTZgR+5dYC1KCC9YKamT/F+TUgZMmWHM\n9r9Q5gJ5O+rzE2IzqlSurPWBFkN8QeUWWyNBmcULRk6JiobXEmKIyu0l+Fn1tdHN\nJwAaXIFXdNu0NW8lAdF7HqtNiU3kUshqTvloggI8sjy2XJ276M4QXVf51B5xXnmM\nbwIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEYCIQCs8QCxH5JY/X2zOWA9RNyLnKhV...
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
MFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAETD7iYtMbQ5Pah3vJbI9nEJWL/Lw2W7Mj
CGcgcpijNd5F1Wsk0qu64m4x8rB20Zxq6qVZpbU6ydh71z1PRJWJqQ==
-----END PUBLIC KEY-----

  RSA Public key: -----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3/MsrzR0G18X0tCH35Cp
giV1px0IjSpqP49MQajyTcpSaOIFjvi4QtaHo3VsdAjXnBI/jp/NAgOKPIGONdVV
xyCLH0tClHqCL9GqZX0GiPEIKT8KhlArgRHt05JRcHLJfdHyWPYDDRtYnHF4eb54
SuMpHfWUdOffYhFHnC9NVRK7qj1FvRkp1f/TnVWzj4/D41BpWLx+uc5X/xJR2aNW
coroaiVWZaPt8LWugHZBoIK02SAw/KDyQNXcBKuXRYt8dY89dxwaKfUOfqoslKpp
+DxxpsmHzx2kYIVkaLeq0VjLUr61QDj9j2yg7X5Z4nKzBlsuY35jbiD6AkUl2yFm
twIDAQAB
-----END PUBLIC KEY-----

  Signing data for iphone_5...
  Data to sign: {"device_id": "iphone_5", "public_key": "-----BEGIN PUBLIC KEY-----\nMFYwEAYHKoZIzj0CAQYFK4EEAAoDQgAETD7iYtMbQ5Pah3vJbI9nEJWL/Lw2W7Mj\nCGcgcpijNd5F1Wsk0qu64m4x8rB20Zxq6qVZpbU6ydh71z1PRJWJqQ==\n-----END PUBLIC KEY-----\n", "rsa_key": "-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3/MsrzR0G18X0tCH35Cp\ngiV1px0IjSpqP49MQajyTcpSaOIFjvi4QtaHo3VsdAjXnBI/jp/NAgOKPIGONdVV\nxyCLH0tClHqCL9GqZX0GiPEIKT8KhlArgRHt05JRcHLJfdHyWPYDDRtYnHF4eb54\nSuMpHfWUdOffYhFHnC9NVRK7qj1FvRkp1f/TnVWzj4/D41BpWLx+uc5X/xJR2aNW\ncoroaiVWZaPt8LWugHZBoIK02SAw/KDyQNXcBKuXRYt8dY89dxwaKfUOfqoslKpp\n+DxxpsmHzx2kYIVkaLeq0VjLUr61QDj9j2yg7X5Z4nKzBlsuY35jbiD6AkUl2yFm\ntwIDAQAB\n-----END PUBLIC KEY-----\n"}
  ✓ Signature generated: MEQCIBDFpNCQeasP2mmV6+wt1PGGnnbA...
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
  Data to sign: {"device_id": "iphone_1", "shares": {"iphone_2": {"encrypted_share": "M+16gXMGJTypoyZ98YZ+KU+0Pv2su5jYWSw8IpYqDp5InIMBRAydHdygrzo5DJV4", "encrypted_key": "opLu+Z3q29ESB1twmUOx6+aRM9C1xQe3fM+dg5R/vHDcLICjOr0dr8gLWi6Bd9qwfglQlKrPoG71DgnJyyQdKo7NyY+yn1smSJSMr55KlJ5sRTCLW0RJOGy01kdVS4dcDmRUQJ4GEL/ZH2vaSoGhHgmfsrlUbRJm0a3k5ASxxv6QhIZLwbgwJ++EmSus40ufba+ZqvajQY7J4VuNMCOfTG91ornXeGCRYyHZdbGAaWVTq73vtqq4LQa1gM04Do4On8cho8LjxkM6em8SccPINtrAYpTErBXuU3+YyRwXBpnqwH9iP751J8fzTKp3Rk+rA5Lu7LvOxJb983ZFjyJuBw==", "iv": "rm9bU0ZNGx2YLvX2yNTe5g=="}, "iphone_3": {"encrypted_share": "XtOXG/VeqZPpb2gyKR6jONeGTNs6G064kzpV8dkvb8ukFrJMF/VvsGPNB5W6sfaV", "encrypted_key": "TKhNFz0OgZw9Z16t+4bZeJcjnxliiw2Rulv79nXh2N+YFCJCUrelWM81unUexlhxcxLJ9+i0T/v0Fs9D0zBrzvpAe1zQIJK4tO6huLqKGsBM5H288g3GtIja2MssLGNI4W25nrEQRo6tlHAPvaE4w2YLyYWoGQcFzAiG/4TtV3KEtVESTZLVXaMGR0XTjd3eyMIO5pVdZzAgOUqa6D2XV1TMpcG3KOK3RZjS9n5s91d9Mqqj2KggIh11HzzGu5tF1R5T3W/5m9A4HSM3HCzr17W7JTnBgXuO4BXHZYbFoipYO68qi3E5VkTcfyGtWrQ00G/7vkEO0IWYxHz8cLmWmA==", "iv": "7VQzrPQ41z/EgYRhe6Cw9A=="}, "iphone_4": {"encrypted_share": "J/GGfFRdcukt+orfoQ6As6iKbv/yv9OIkhDomAaTKsUQBjGY/EXkSZdTEXjozC9R", "encrypted_key": "BWIcFU7hu7ezQexvqdgSfh8pU3jBbmlbR67fQ9gXy3im98zXSvEmZYk7Iz+MxmLxSVoPjyLmqxwt9m3BfsjFs2SVpNTNCq4TliK/xw7P2vOGbvuCXSXiF2BomQ28z/EMRzCRaGif/xjWtcLxFadH2BA1XAm0Rt9C8GNOegh2IwJixstvSN/xSC0pRck1phV7HSOiWsFuCspYChLebcIie2LJ/AOA7CoiHrwCsn0SSWdDVKfOhdqerXpbK/A3YPOcfMZVn3fSuJDaeFjBQ+06JaTz+QGo7BwPzoAWXFQbVr4MW5Hcy06J3St3ZI8bPxs+DGE7obEMzJP6hC+7O5PUvQ==", "iv": "cIvvsgMo6mLgiSLqaEnL/w=="}, "iphone_5": {"encrypted_share": "hw7EbDUxD9GRG1K9EvfDvRQeMwe0FIgMTvlpFECry5eyUVMnehl4FKCkzV/p5TOm", "encrypted_key": "FSCNyp9IBlE74SJaEjwPuhz/TSxazbEwZO71PiOck1LgjNNm7LXeGqxBMnF7HuPbSDc7cPeW9iIERjrUjDBA5wg/g/3RUVtFVQ3XBUYvhcJF4llf6AUZBczZua8XZKmDnY641qNVO3j0NquBoDkosEz4bZJu6rNbWOdTrKFcRpDwbxbCGpwS2obGwr2Jqhdjgq9ePxEXNMHtuVNwSN8dZZR/n00FJ3WF0VeTqHKJJGyAdaGsXFddjoroB8bflG2/3m4thp7S6ggDmrG+KcMOIGwKmJf9IfMhlFmcbtxpy3yBgD60DR28qOV2HHqXe0usIE6F/DmQjOTiSgBNcHXW5g==", "iv": "jz4UFbAqk7tXGdaw+GYJkg=="}}}
  ✓ Signature generated: MEYCIQCc9dQ/kEPwpMqTRiVyJsEUeJWX...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Server response status: 200
  Server response: {'message': 'Shares from iphone_1 stored', 'shares_count': 4, 'status': 'success'}

Sending iphone_2's encrypted shares...
  Signing data for iphone_2...
  Data to sign: {"device_id": "iphone_2", "shares": {"iphone_1": {"encrypted_share": "KOhOWcfFrWj06XnBbWCPNYT92qnCfbnVda+hvoi2lWtbvRjg6gss8DsJo+Ehq9LG", "encrypted_key": "OfjEYjg/q4QwIad65L3rSTN5pnZMbIFy5umU+BHAgV4ThodJb6DvYlZms/PyEjFgN1UwLqx7KYpGX2iZMLZH8g36PXsFAynh4Wkc/WhXoQD4tLKOaTmnsyTHKodGfLUeXCZWlpry5ShojVHZ7EERQvaRMYSiP64ZFXCknr4RTdlswW3nFNUNE9sbaZaDQSnbN6Egc4LLX329Bgzt+hN27KXi40DMaQtQqqGyx06KLra9ifUn9gSGlgZjlwIoQyODRv9OIchJW2vJAyTcv0JLGFWL8/HJDHfGaVQeBDkYoEund852wOp+AO8tNzT+0iL2LdKsdxQEXLlFCcppTVBNnw==", "iv": "VXOE063y9B7zEo5caaZKEA=="}, "iphone_3": {"encrypted_share": "ff4sgCyLGUeEp+e5WTd/ORnbYrOcR5JBZVdgqkmfM/MH3driQ5/maahgqSX+JGZY", "encrypted_key": "V3ndvFZHOePMz5Uki+8ZR4CYRc6RCypGWwWhmT5HJmzkL/F4YRCer3LMfyWhuS3+ShSq2OqQenhy9LBskK+eGnUpO/mZiYQfHxacjrO/5OaQwyatj/Isy+FLf7Md/+6/odSbUsHr2LJA2UC1epW5dOApW6dMukq7YeiNvew5cUWTg/wsfc7hw3HsFht4f8iJNJk5tok1M/iziCt2QkdJY96uxm7d1EAe1Fe2mvhnLDK6vU1qSQ1fxAIyut1d5pFaFD1zc8wMog9PnYTgekFOOMu2wlYclchY6RXBtTFW5aB+bgzuSZ7DElFQVGKDH9wZP/g/6OIwcETpCSLu1pGUqw==", "iv": "3nmr7+UZkC8Gc0ed/RnhxA=="}, "iphone_4": {"encrypted_share": "IDA8hx2UmhapxttSk+tlp38zpczv2oiNVo1U0PlblHxIzQL5vOu+ieaAgITplu8e", "encrypted_key": "KMvbIRrQYbpVKHNZR3ufuEjMWvH3F5X6Nlp9UHvG41u+FYjmRJKoJfg0oucMTK1pco+bbGb+HCQsQtQYX8B1v6PBbROVJe4H1A3lQihat68RqQYEJKPbza7m8M4U0ay/6XykH35VbTH7I7KZMrwWlsv8qaPp4rsQXEuRGJ+6J8s5Jz3XLjnAoGeDVtDHGIWR0ewr9+gitCX7ZOfbjEuTi6o8EYbn0vNhLezhitD5R8Altd1lQ+93Kq2HeCExd4iCso9waDelSRzEERrVX8Bc/YohLXosYfEe0OtgZ0/AhbTxIrmiBW4ENX1QGag3mm1u4fjOv3OtTp3lkXaihDDdcQ==", "iv": "HSuBKwPZHmqY0Gcw6y/0eA=="}, "iphone_5": {"encrypted_share": "TxRh4vSQlppAZqX1MF98ecHC3Z2ZALpOX1XprY+BNVP8g1DEvT/9WhsrhoysEDKJ", "encrypted_key": "H8v9IovzrNWGZQROiaeN0SRGq3vNzVSSrUPIq6so1wNqC66hHHlZsFTUqDLZ+Ddq3VcxuIzTwZz8ZFB6dmcCq9z2CTEFGJvui7tYyG289Ov5tYU52sW1ZGI8MHJYWxyNRFOmlyfFbIXAtSeTuEOkgDPhQQPiK4W8JxMsRU6eGGg7ZX8N2fWzBj9AdQAFeJP4zxk8Qr/0f0pG9LE/30jz3vC8sansZij8i+dMybIK8CdzEZ/A3f5Nm09r7GXuiqtLeEvasMNl4p4iGZRCBkCdMtXB9okARn/W7u4FQh5rw6gBhJgbLUdMYCIn4AdL97KiSs5A+HNkjZgibe8pDClmYA==", "iv": "tyL+PXmNcMrbXUxPhFDX5g=="}}}
  ✓ Signature generated: MEUCIQDPdm4nCPGsGfb+KnUGKHp87sTr...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Server response status: 200
  Server response: {'message': 'Shares from iphone_2 stored', 'shares_count': 4, 'status': 'success'}

Sending iphone_3's encrypted shares...
  Signing data for iphone_3...
  Data to sign: {"device_id": "iphone_3", "shares": {"iphone_1": {"encrypted_share": "JkHrXMSwuxZVU24Fx4j0L5F7RKnCcAaWut9c4nhhGEyxxIyB3AOAX5W8qw+jQ2MU", "encrypted_key": "iq+YjUmn/KmFeOQ1uuvKBezeUs4/12kEoTDJrM/ySs11Ek7nEvRQk7wuVY2C9mktQsSPS6XzLP4hEjtU6+irF4SYB8RISGO++KC4wHuB7P/eRrlP3z+IVzrgWsx2KVUkkWoJvV6ZjRd01IH7SlW19qbDsOuMvSklM8uAnrqw4CE/i5LZ1wN7rfUpJL3PfPOJwMhYfVHunFstefb7sk7sbJIE6a8mTWn2N1rAv5nki81jwxjnAkbbDSL22Y1SUK7fMEWwQP+V2ZNEv309NSq2tFldkEY0gQWi+/9kXkq9SC8p1ROtSzYEmL+jWO6QSmnTu5mrDHBfuOeUz+An+7kbvg==", "iv": "qo16/EfiQ0XinS9vkqD1rA=="}, "iphone_2": {"encrypted_share": "nIoSdA1GEBAKf0WnRLRDH6ttyCDYB7KIBnfkpPutwd7cxv51yCjNYfvZmvUdCyrs", "encrypted_key": "P6/T6z6KWthW9fowqK5qy6fFuxPlKsYulgEn2jKCIsc+R5kPakQ5tdqZL7dg8cJIVlbr9DHiO4wQTyg9h6++G0uUvU4M9Twh6oPN3LLBhgWkbqqZ95xn/acVtUtpO201stbqI7hXBpfdrfCsbrihNwQH+j92rOfWOwgpUp5XP3noj4XipktgsGM0uBXJBZJhdzrCRgViGwHW41/QXtEoB8eK7qpL8XoruOWRKY1KsrPk+K/lrSwpgdKLcHNJgqBWaSjTvkxGne37yeAWA2RzXJdIn1MdKh9LoPAIDb9a9HDS9aPLveEXEt6UtKBmNfdS9JjgcrIRX6DAIloYnfHrRA==", "iv": "BkcTK+gEl9M16s6L7ScIQw=="}, "iphone_4": {"encrypted_share": "fjPvpeXZFGksxPPlZCX9eJpO0f7yiA9MzUS4TTurBBzt3qwruTyeifkHRV5lOCkp", "encrypted_key": "zllqzQxqSniXkDfXtW6DqDZ/FyZJt88/7toAdbvr7HnP7GAjP14JECBUh9kuGnR5/O5KuKkZle9v+/XS/Z5G0+41BoNINuXiYTROcFwmkPXXFhenbYWeIyCl49BF1BOBW6zIYqQ92ckzkGKAGfJS87/WRb7gN7sxUJuijKue5P77ZOoYheUsFTa0vC7ElylGO33qi2wRvSmZnLPOXR1Uv9iDYX3edameW+CacLKaeY9nGDXiBvUHfi4bavcYTy+k11EZcPIMrqM0cq7g7r3syC+/vA1U+flmGPgYLOyT20e1OmV6VzRAeUoP1NA6lYG5R4t9zwzpqGLRQ/9g6H4Hcg==", "iv": "BdBtLY53UNf1kRloM1kgPA=="}, "iphone_5": {"encrypted_share": "F85xXTVnl0ZHTs1e7VlwVBKCYFWKfCKhZFYA3a4Ek9u77bnlJ8ouFHKXxcDMcL7g", "encrypted_key": "OivZb24Rhd5f4++6WmwPPUx9G90VhJneIZZHkpFie93SY8/PXrr01Huwj4MtgJ+xWhKiE1uRatPhJtiPx1On5WV34KXkJhy2ANUwHPC+0k3LIMi2VykUd7iCSHK4j8GYVC5FQsc/+F2fVXdspv/J3PhmWH6UweHlZEMEGYuQ/3N8mxQhz6jNTL75haDLUGw+x/5mWGHX9XPbcFMyx5OOg/z4JkV3u1E9SonUDRpVX8kxV4aZ4Ae1clZTPqcnXTaW18KwGYbdEhv7N+IevqWRGBVflsC0GjwyxsKaoATG7LhhzNfBlnLzuHQVyQPlpLXb75zzwx+DqmRwe6ww2hz8oQ==", "iv": "c4l32V9oHPOOm6J5UY9OZA=="}}}
  ✓ Signature generated: MEUCIQDCj0gvhbZW2WXKyooolNnLE7jm...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Server response status: 200
  Server response: {'message': 'Shares from iphone_3 stored', 'shares_count': 4, 'status': 'success'}

Sending iphone_4's encrypted shares...
  Signing data for iphone_4...
  Data to sign: {"device_id": "iphone_4", "shares": {"iphone_1": {"encrypted_share": "I56fCf1V3cuaNvtNI/86eH+kfZ199Ka96uTvMbR9JCfE3WSYbHu1UA86cTjpx++k", "encrypted_key": "dBUobOchiWmAiCHVudKigEowZ88WxDVOKCHLYL5lMQm365kE+fZP9sV5F8rGgwg9cnGqzpw6Od/WkaAX/fWQKTaLAHzyHTZY6vWAKpHmg3wR3syQjN5BIL+mB0H7ikYVPsJDQBKpvsQXzcSTFvAZR6Q2vuVHxsdl+IxUY+o+TRcEQtXScdtW+pnJuUDKL0COtam0jKr4OuF1+68FWHRQrCHStY0p0ReBE6w/P9cip5Nw6VLYHF/yYjvtQAl1V5XJswZanM+HM0AinwkC74G0G+z5LphmaNBPSpKpMO6HI58WYdd3E1EJzSKdsRFhIrypzxZKan1b8W3A3D9/I+eGEg==", "iv": "9fW0uGtqH/c5d2fIBTdBBw=="}, "iphone_2": {"encrypted_share": "7JZJA/z9Iw6CBQh4qmKxoRGDnFXq04MXWYOLWrCRunU5xQjwS6yx3F9IMduXqd+L", "encrypted_key": "LMR4VksxbXI7vddnm4z2ztaweXev42f87UnvQCJRqilEoilFIel51TjPkZfrb3mjzfImvczny48fBVWFT6rjZTWBKLTmg0wJQS/hYaDqDkF+zvxUxX/MDIhv86NzBpFrbFqUtryT0pePKmohNntZa5kk1LLAXwy1gd7AFVMV/4Vt29uqQy0lFEEyjHXMWizcy3tPeRqB3B9xatNmPHjA+g026aZBvVeX8pY/jtFu/Ir8pEanKnMUjNS+xRMXGl0Xu4VgFr9TaUOp+SBW2RfWd4kkIDMvhIkI11SBgcn6Y+PscmXoBax9y3CuvDIKvHZxPOJ8EIK6PQNgy6i3yfI08w==", "iv": "RgJINp2NqE3TeisUlv3u/A=="}, "iphone_3": {"encrypted_share": "JB1FZ5h2rAL/wfHZYP5wXVJUPMV5sVHHyIlZ2+e9fGfYr0Swobnyo/CN9Zb2MwjR", "encrypted_key": "UOe7KD98X/Vxtg6jnHHv7PP1g6EWCfjcjIE43F/+sAZ18J0vJE05hpMeQl83pm+tTsk2ETttr8QriOIaAfA3ZsVu0Bv6+70oPiaioTLJHzUszinmhENwkLnHHhFiGIVzupLm+qyQ25RNvRY/MagqDUJeA7agwIzUbZcUhh3T/TA0riHI6eZ4gPsonYpQqRlcSJ8dKO42Vjh3ub6ecHRlbsarmXdH5Cqv1yNKRKjLh3wTWlAr5ZKsl4/caovq3RXChZeuZ8LHp2T5PC9VQKX3ftBGjDGMNKCQhMwKuzow7g1plMZS868Dd7B1czoxd9Ok9kE3Zkr1EPXoD6uuxebF4A==", "iv": "0+jv/8lJD6ChnJbxm0xRVw=="}, "iphone_5": {"encrypted_share": "ZrvrnILsm/D/dRRZNJSNmX2POMT87Wk6dmd9u9skREKLJoVk/5LyvKlTB5WUX0lv", "encrypted_key": "XxQ9Ci/DIOpnOoDWPAgYOPmtj07pUNZrvjSGo9K6ebUCfVBXNiB8qhidCEM6vMCt675jzPljVONQBn+kF55Kn3Q6ReKHMNDpxlt85sgOYDYJOpHMuWwYgCszpTBEt7ymjLxQ124IEQ92ff4cjFMK3P3R2Ic/uWZs/+e6VdKh9MIG0iSTRqknQ4CRR0823Xj/QElMB9c75KJPvzLJ1gC2qw8CBEiO+7SUa3BgGFRbYgnhxlc42wCrijBCUPGMifXF6Dp9Tg8WUJzsSbB4UhNl8yCPqR72PnZTVW5hZy7NNjs7vKAih01WcoWhtdI1/Gt/hzq4q6QVBt3xO0XtZh8nGw==", "iv": "vYBhqRPxSMNWAM1gMVGXIg=="}}}
  ✓ Signature generated: MEYCIQCcxgVSfmc+96/kSu4nkaOmfzoT...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Server response status: 200
  Server response: {'message': 'Shares from iphone_4 stored', 'shares_count': 4, 'status': 'success'}

Sending iphone_5's encrypted shares...
  Signing data for iphone_5...
  Data to sign: {"device_id": "iphone_5", "shares": {"iphone_1": {"encrypted_share": "OMRsDKJwOZadWcADAbBqYDrVs3+c5r9NC4aj3/TnQoJO6iYhTvu8rXTMtOhTdnMP", "encrypted_key": "NHS+kvQIqb2OlQ2jwGctYe7IUP9m1RYcC4yIWBDvkvFZ8DMZw+1AaT5uVid4WilFny8dK01Ub1iNF8ICqZtp3eniZiDXF6ne7GdDaRVMVQdR7Wf0cnH55/YDoiYaF5vMbxldPeoFEKxurf42KxXMU/XM1GlLQPa8FixU3h7RjPh5D7m2p+ay7k9uAhOngFt3SAxQ24FgZQIYQg8zMpRbbno5Uw5EqMhBsYpXufUC50V09oxq2MoTNWRc2JHKwHASamO9bYsElc3LsodfbHbipUrMJ5KAQ2nnMSFyfYW4MqWg/qukmnYOQs+4eCXyz+QxI+HB6C69YqrzUgPsfIIRow==", "iv": "Gv/LUBas4myOMkkPcMgppg=="}, "iphone_2": {"encrypted_share": "3lhG94n3wYPXuh7zcZWakY86iIXZKFZxfMYV79iiLEeePvM5Cl+Bt1paBgpgSSHg", "encrypted_key": "jm5UCnZoyaVDWdUe6lYZ26/UPKbHH2HRQcmz9ywbGzHSpYeRaKFcrlr9glUiKXZJtnZ9Ok9N2ilFyZwRRmlrabPJFpNS2jCMBoIptGVg4fem1LgkE4+6sjvoXhXLOg3FfQh8Or165aFfJpj/9x0sDkFJaEyM23c+hcH/b9Ocy49Y8KdEDF61yJX1d800MJBgdM82SfbPoEfPVoA2IsyKj6N+JcUG5xfvmYGkHW6y95Q6tGObsQQNB2ILocD/wCnK9uRfHeV90xjVZ8Zz7R8ujPZENhtf3AGFNb/q3bft4CKpfqDnXFfFSCTY3QvvbcGyrkCjzjlJS4b6xKtYwDAI1w==", "iv": "Gn9DKRU7qrs7wtZQuyJ9og=="}, "iphone_3": {"encrypted_share": "AVNFUZOJN35DO71OXz0T3jVEEgWXFc2aQuPvAzjrvD3ISJ5K2940+zJwQ05Sbj1N", "encrypted_key": "ixZoRS8NXwqaxXE+5TspvdvU5ODLthAF41E0CEbo8x6CMWT5+KsOc7FRp96K8ZmKRihUkUJb19eL/IEp/LAvJWF+cBOoSiVk3gcY92/4rYe6eC2bnnJUXIjesFc0D7IC5LA0seEd33xUi4dVldqnauHyJ4nrGL6khVafLG7vc1vNDnJrN3JhM2TDQunchzm/mFi0zgV7fIFSe1WIqVEM85R0K16IAbETb3drB0rcudpWBJJ3nzG8jIV6xjceTMnhjqwXGQxZCuMFUvrNu9HMFUq1CmIInwX27LmMgQC8aV2G5Ro/CQwjsUNxN8ADLc1nhqT6G9mWgbqQyCfY5WPFCQ==", "iv": "PWbwngP3Db+Gdht5WO+9Rw=="}, "iphone_4": {"encrypted_share": "RU6AhJWL7hnm4qFwtZwnhrGF6+q1rOQJdoqYi+eUvfm9Ge1iOGmtuZKIllLDLFKJ", "encrypted_key": "Y7YhynlWfSwr/SPHRQMBOuGx1b61BWFrMJ1YvjO9DSmrBLYVu2zW6jkqx3ucUi7QhRd9PFuMinzjdXcXW7EdL4SmS4BvoOFclVvirXn4Mzzz6idjmu3jthm7RYbCj5zizIyphB4w1ab7q6sHHBGPWU7hjOJuyN8P+13HcWqGxeZheMVVfjXO2SCUaIDr2DAlUw4itq2z1DiXI6wIVDL+xzxnCI5LqZAxKuoDBcoCVOKaoSbv0OCjgUFX1/MOfcebw0UU6o09xMGBKH1aSCMH/eCwG9s5jmgPLiiTu1SskmG5JKPtWS4rAUZh/Ehx+rQW8e/D/wEUMDnnGF03RW2JLQ==", "iv": "umjtQMdGPkdhznZaP+D4sg=="}}}
  ✓ Signature generated: MEQCIA4GeFj/ohZEVzbhGPtCZ21aVblg...
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
Threshold wallet address: 0xbb63b98e4588ddf8dfb0674f6a0bc52eced0a155

=== Collecting Partial Signatures ===
Need 3 signatures for threshold...

Device 1 of 3: iphone_1
  Signing data for iphone_1...
  Data to sign: c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160
  ✓ Signature generated: MEQCIF6LfrKCz3Pi4cthnCg1JFgwS2d/...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Partial signature: MEQCIF6LfrKCz3Pi4cthnCg1JFgwS2d/...
  Length: 96 characters
  Raw bytes: 70 bytes
  Signing data for iphone_1...
  Data to sign: {"device_id": "iphone_1", "partial_signature": "MEQCIF6LfrKCz3Pi4cthnCg1JFgwS2d/CAobL8kw2feHDRGuAiBW2SM57upDG2ym/vxeqK/hhOcHiwHIVIcGPYpXPmsl4Q=="}
  ✓ Signature generated: MEUCIQDypnnQhcKB5jBNZNdYWq45yB9q...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending to server for aggregation...
  Server response: {'final_signature': 'MEQCIF6LfrKCz3Pi4cthnCg1JFgwS2d/CAobL8kw2feHDRGuAiBW2SM57upDG2ym/vxeqK/hhOcHiwHIVIcGPYpXPmsl4Q==MEUCIEXSh699YZB+77bI+fc9r7rCcfu4TCSVytdHGz9xKAOpAiEAkLrV87mNg6nnZCxwvLkE+SpNbig1ICVbOQjUYeTM9Ho=MEYCIQCsRBZTRz3Pt4xKFLhb5HYa0aZ8jlwSPAuza+1OCpkzLwIhAMXcXLO+9ShM/cyo2GeDg4RF39E4uokfbnrNajujQOX0', 'signature_ready': True}
  ✓ Threshold reached! Final signature ready

Device 2 of 3: iphone_2
  Signing data for iphone_2...
  Data to sign: c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160
  ✓ Signature generated: MEUCID+frNFiwSsaPR94K0z1gp9zdqJq...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Partial signature: MEUCID+frNFiwSsaPR94K0z1gp9zdqJq...
  Length: 96 characters
  Raw bytes: 71 bytes
  Signing data for iphone_2...
  Data to sign: {"device_id": "iphone_2", "partial_signature": "MEUCID+frNFiwSsaPR94K0z1gp9zdqJqe+DaZLHa5jrqD54RAiEA3tUACrhkAkVRCmmE5kPhR5WJud9EsXkXs2gRFV94InE="}
  ✓ Signature generated: MEUCIDKNA0F69eJUj+i/R0YgZF91rWOZ...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending to server for aggregation...
  Server response: {'final_signature': 'MEQCIF6LfrKCz3Pi4cthnCg1JFgwS2d/CAobL8kw2feHDRGuAiBW2SM57upDG2ym/vxeqK/hhOcHiwHIVIcGPYpXPmsl4Q==MEUCID+frNFiwSsaPR94K0z1gp9zdqJqe+DaZLHa5jrqD54RAiEA3tUACrhkAkVRCmmE5kPhR5WJud9EsXkXs2gRFV94InE=MEYCIQCsRBZTRz3Pt4xKFLhb5HYa0aZ8jlwSPAuza+1OCpkzLwIhAMXcXLO+9ShM/cyo2GeDg4RF39E4uokfbnrNajujQOX0', 'signature_ready': True}
  ✓ Threshold reached! Final signature ready

Device 3 of 3: iphone_3
  Signing data for iphone_3...
  Data to sign: c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160
  ✓ Signature generated: MEUCIQDq5HGe5HHpBRFrVrV1LyGmhW1g...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Partial signature: MEUCIQDq5HGe5HHpBRFrVrV1LyGmhW1g...
  Length: 96 characters
  Raw bytes: 71 bytes
  Signing data for iphone_3...
  Data to sign: {"device_id": "iphone_3", "partial_signature": "MEUCIQDq5HGe5HHpBRFrVrV1LyGmhW1g91E8q18mLWHps7eOPgIgL1nlwUiWrLBPV/8L+MufUBmX5jn4Bj7qCLbN2Cq98Gw="}
  ✓ Signature generated: MEYCIQCGUnCKGSgmPAp2E4rlhRxbiO35...
  ✓ Signature verified successfully
  ✓ Signature verified with public key
  Sending to server for aggregation...
  Server response: {'final_signature': 'MEQCIF6LfrKCz3Pi4cthnCg1JFgwS2d/CAobL8kw2feHDRGuAiBW2SM57upDG2ym/vxeqK/hhOcHiwHIVIcGPYpXPmsl4Q==MEUCID+frNFiwSsaPR94K0z1gp9zdqJqe+DaZLHa5jrqD54RAiEA3tUACrhkAkVRCmmE5kPhR5WJud9EsXkXs2gRFV94InE=MEUCIQDq5HGe5HHpBRFrVrV1LyGmhW1g91E8q18mLWHps7eOPgIgL1nlwUiWrLBPV/8L+MufUBmX5jn4Bj7qCLbN2Cq98Gw=', 'signature_ready': True}
  ✓ Threshold reached! Final signature ready

=== Signature Aggregation Process ===
Partial signatures collected:
  iphone_1: MEQCIF6LfrKCz3Pi4cthnCg1JFgwS2d/CAobL8kw2feHDRGuAiBW2SM57upDG2ym/vxeqK/hhOcHiwHIVIcGPYpXPmsl4Q==
    Length: 96 characters
    Raw bytes: 70 bytes
    Raw hex: 304402205e8b7eb282cf73e2e1cb619c28352458304b677f080a1b2fc930d9f7870d11ae022056d92339eeea431b6ca6fefc5ea8afe184e7078b01c85487063d8a573e6b25e1
  ✓ Signature verified successfully
    Verifies: True
  iphone_2: MEUCID+frNFiwSsaPR94K0z1gp9zdqJqe+DaZLHa5jrqD54RAiEA3tUACrhkAkVRCmmE5kPhR5WJud9EsXkXs2gRFV94InE=
    Length: 96 characters
    Raw bytes: 71 bytes
    Raw hex: 304502203f9facd162c12b1a3d1f782b4cf5829f7376a26a7be0da64b1dae63aea0f9e11022100ded5000ab8640245510a6984e643e1479589b9df44b17917b36811155f782271
  ✓ Signature verified successfully
    Verifies: True
  iphone_3: MEUCIQDq5HGe5HHpBRFrVrV1LyGmhW1g91E8q18mLWHps7eOPgIgL1nlwUiWrLBPV/8L+MufUBmX5jn4Bj7qCLbN2Cq98Gw=
    Length: 96 characters
    Raw bytes: 71 bytes
    Raw hex: 3045022100eae4719ee471e905116b56b5752f21a6856d60f7513cab5f262d61e9b3b78e3e02202f59e5c14896acb04f57ff0bf8cb9f501997e639f8063eea08b6cdd82abdf06c
  ✓ Signature verified successfully
    Verifies: True

Aggregated signature: MEQCIF6LfrKCz3Pi4cthnCg1JFgwS2d/CAobL8kw2feHDRGuAiBW2SM57upDG2ym/vxeqK/hhOcHiwHIVIcGPYpXPmsl4Q==MEUCID+frNFiwSsaPR94K0z1gp9zdqJqe+DaZLHa5jrqD54RAiEA3tUACrhkAkVRCmmE5kPhR5WJud9EsXkXs2gRFV94InE=MEUCIQDq5HGe5HHpBRFrVrV1LyGmhW1g91E8q18mLWHps7eOPgIgL1nlwUiWrLBPV/8L+MufUBmX5jn4Bj7qCLbN2Cq98Gw=
  Length: 288 characters
  Raw bytes: 70 bytes
  Raw hex: 304402205e8b7eb282cf73e2e1cb619c28352458304b677f080a1b2fc930d9f7870d11ae022056d92339eeea431b6ca6fefc5ea8afe184e7078b01c85487063d8a573e6b25e1

=== Complete Ethereum Transaction ===
{
  "raw": {
    "to": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
    "value": "0x0de0b6b3a7640000",
    "from": "0xbb63b98e4588ddf8dfb0674f6a0bc52eced0a155",
    "nonce": "0x0",
    "gasPrice": "0x04a817c800",
    "gasLimit": "0x5208",
    "chainId": 1,
    "data": "0x",
    "type": "0x0"
  },
  "signature": {
    "r": "0x5e8b7eb282cf73e2e1cb619c28352458304b677f080a1b2fc930d9f7870d11ae",
    "s": "0x56d92339eeea431b6ca6fefc5ea8afe184e7078b01c85487063d8a573e6b25e1",
    "v": "0x1b"
  },
  "hash": "c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160",
  "from": "0xbb63b98e4588ddf8dfb0674f6a0bc52eced0a155",
  "serialized": "0xc5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab1605e8b7eb282cf73e2e1cb619c28352458304b677f080a1b2fc930d9f7870d11ae56d92339eeea431b6ca6fefc5ea8afe184e7078b01c85487063d8a573e6b25e11b"
}

=== Transaction Components ===
1. From Address: 0xbb63b98e4588ddf8dfb0674f6a0bc52eced0a155
2. To Address: 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
3. Value: 1000000000000000000 wei
4. Gas Price: 20000000000 wei
5. Gas Limit: 21000
6. Nonce: 0
7. Chain ID: 1

8. Signature Components:
   R: 0x5e8b7eb282cf73e2e1cb619c28352458304b677f080a1b2fc930d9f7870d11ae
   S: 0x56d92339eeea431b6ca6fefc5ea8afe184e7078b01c85487063d8a573e6b25e1
   V: 27

9. Transaction Hash: c5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab160

10. Full Serialized Transaction:
0xc5c9c9b09cbe03afffd6dee3c5a5964f7f2596e4c337bfc9effe7d94192ab1605e8b7eb282cf73e2e1cb619c28352458304b677f080a1b2fc930d9f7870d11ae56d92339eeea431b6ca6fefc5ea8afe184e7078b01c85487063d8a573e6b25e11b

=== Final Status ===
✓ Transaction is valid and ready for broadcast
✓ Signing address verified: 0xbb63b98e4588ddf8dfb0674f6a0bc52eced0a155

✨ Test flow complete!
