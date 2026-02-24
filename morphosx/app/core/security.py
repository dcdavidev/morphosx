import hmac
import hashlib
from typing import Optional


def generate_signature(
    asset_id: str,
    width: Optional[int],
    height: Optional[int],
    format: str,
    quality: int,
    secret_key: str
) -> str:
    """
    Generate an HMAC-SHA256 signature for image transformation parameters.
    
    :param asset_id: The unique ID of the original asset.
    :param width: Target width (or None).
    :param height: Target height (or None).
    :param format: Output format (e.g. 'webp').
    :param quality: Output quality (e.g. 80).
    :param secret_key: The server-side secret key.
    :return: Hexadecimal signature string (first 16 chars for brevity).
    """
    # Create a canonical representation of the transformation parameters
    # This ensures consistency: order matters!
    payload = f"{asset_id}|w{width}|h{height}|f{format}|q{quality}"
    
    signature = hmac.new(
        secret_key.encode('utf-8'),
        payload.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    # We take only the first 16 chars for a cleaner URL, still 2^64 variations
    return signature[:16]


def verify_signature(
    asset_id: str,
    width: Optional[int],
    height: Optional[int],
    format: str,
    quality: int,
    signature_to_verify: str,
    secret_key: str
) -> bool:
    """
    Check if a provided signature matches the expected signature for those parameters.
    """
    expected = generate_signature(asset_id, width, height, format, quality, secret_key)
    
    # Use hmac.compare_digest to prevent timing attacks
    return hmac.compare_digest(expected, signature_to_verify)
