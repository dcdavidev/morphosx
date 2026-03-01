# Security and Authentication in MorphosX

MorphosX is designed for security, preventing unauthorized access and protecting server resources from Denial of Service (DoS) attacks based on arbitrary parameter manipulation.

## Signature Validation (HMAC)

Every GET request for an asset **must** include a `signature` (or `s`) parameter. The server re-calculates the HMAC of the URL and compares the result with the provided signature.

### Algorithm: HMAC-SHA256
The server uses a shared `SECRET_KEY` to calculate the signature. For URL brevity, only the **first 16 hexadecimal characters** of the signature are used.

### Payload Construction
The payload is a string built by concatenating parameters in the following order:

`{asset_id}|w{width}|h{height}|f{format}|q{quality}|p{preset}|u{user_id}`

*If a parameter is null, the string `"None"` is used.*

### Python Example for Signature Generation
```python
import hmac
import hashlib

def generate_signature(asset_id, secret, w=None, h=None, fmt="", q=0, p=None, u=None):
    payload = f"{asset_id}|w{w}|h{h}|f{fmt}|q{q}|p{p}|u{u}"
    sig = hmac.new(secret.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return sig[:16]
```

## Private Asset Protection

Assets uploaded with the `private=True` flag are saved in paths such as `users/{user_id}/...`.

1.  **Path Validation**: The server verifies that the logged-in user (via JWT) matches the `{user_id}` in the asset's path.
2.  **Signature Validation**: For private assets as well, the signature must be valid and must include the user ID in the payload (`u{user_id}`).

## Timing Attack Prevention
For signature comparison, MorphosX uses `hmac.compare_digest()`, which operates in constant time to mitigate timing-based attacks.
