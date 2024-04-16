"""
Everything within that module is off the semver guarantees.
You use it, you deal with unexpected breakage. Anytime, anywhere.
You'd be better off using cryptography directly.

This module serve exclusively qh3 interests. You have been warned.
"""

from __future__ import annotations

from enum import Enum

class DecompressionFailed(Exception): ...
class DecoderStreamError(Exception): ...
class EncoderStreamError(Exception): ...
class StreamBlocked(Exception): ...

class QpackDecoder:
    def __init__(self, max_table_capacity: int, blocked_streams: int) -> None: ...
    def feed_encoder(self, data: bytes) -> None: ...
    def feed_header(self, stream_id: int, data: bytes) -> list[tuple[bytes, bytes]]: ...
    def resume_header(self, stream_id: int) -> list[tuple[bytes, bytes]]: ...

class QpackEncoder:
    def apply_settings(
        self, max_table_capacity: int, dyn_table_capacity: int, blocked_streams: int
    ) -> bytes: ...
    def encode(
        self, stream_id: int, headers: list[tuple[bytes, bytes]]
    ) -> tuple[bytes, bytes]: ...

class AeadChaCha20Poly1305:
    def __init__(self, key: bytes) -> None: ...
    def encrypt(self, nonce: bytes, data: bytes, associated_data: bytes) -> bytes: ...
    def decrypt(self, nonce: bytes, data: bytes, associated_data: bytes) -> bytes: ...

class AeadAes256Gcm:
    def __init__(self, key: bytes) -> None: ...
    def encrypt(self, nonce: bytes, data: bytes, associated_data: bytes) -> bytes: ...
    def decrypt(self, nonce: bytes, data: bytes, associated_data: bytes) -> bytes: ...

class AeadAes128Gcm:
    def __init__(self, key: bytes) -> None: ...
    def encrypt(self, nonce: bytes, data: bytes, associated_data: bytes) -> bytes: ...
    def decrypt(self, nonce: bytes, data: bytes, associated_data: bytes) -> bytes: ...

class ServerVerifier:
    def __init__(self, authorities: list[bytes]) -> None: ...
    def verify(
        self, peer: bytes, intermediaries: list[bytes], server_name: str
    ) -> None: ...

class Certificate:
    """
    A (very) straightforward class to expose a parsed X509 certificate.
    This is hazardous material, nothing in there is guaranteed to
    remain backward compatible.

    Use with care...
    """

    def __init__(self, certificate_der: bytes) -> None: ...
    @property
    def subject(self):
        list[tuple[str, str, bytes]]
    @property
    def issuer(self):
        list[tuple[str, str, bytes]]
    @property
    def not_valid_after(self) -> int: ...
    @property
    def not_valid_before(self) -> int: ...
    @property
    def serial_number(self) -> str: ...
    def get_extension_for_oid(self, oid: str) -> list[tuple[str, bool, bytes]]: ...
    @property
    def version(self) -> int: ...
    def get_ocsp_endpoints(self) -> list[bytes]: ...
    def get_issuer_endpoints(self) -> list[bytes]: ...
    def get_subject_alt_names(self) -> list[bytes]: ...
    def public_bytes(self) -> bytes: ...
    def public_key(self) -> bytes: ...

class Rsa:
    """
    This binding host a RSA Private/Public Keys.
    Use Oaep (padding) + SHA256 under. Not customizable.
    """

    def __init__(self, key_size: int) -> None: ...
    def encrypt(self, data: bytes) -> bytes: ...
    def decrypt(self, data: bytes) -> bytes: ...

class EcPrivateKey:
    def __init__(self, pkcs8: bytes, curve_type: int) -> None: ...
    def public_key(self) -> bytes: ...
    def sign(self, data: bytes) -> bytes: ...
    @property
    def curve_type(self) -> int: ...

class Ed25519PrivateKey:
    def __init__(self, pkcs8: bytes) -> None: ...
    def public_key(self) -> bytes: ...
    def sign(self, data: bytes) -> bytes: ...

class DsaPrivateKey:
    def __init__(self, pkcs8: bytes) -> None: ...
    def public_key(self) -> bytes: ...
    def sign(self, data: bytes) -> bytes: ...

class RsaPrivateKey:
    def __init__(self, pkcs8: bytes) -> None: ...
    def public_key(self) -> bytes: ...
    def sign(self, data: bytes, padding, hash_size: int) -> bytes: ...

def verify_with_public_key(
    public_key_raw: bytes, algorithm: int, message: bytes, signature: bytes
) -> None: ...

class X25519KeyExchange:
    def __init__(self) -> None: ...
    def public_key(self) -> bytes: ...
    def exchange(self, peer_public_key: bytes) -> bytes: ...

class ECDHP256KeyExchange:
    def __init__(self) -> None: ...
    def public_key(self) -> bytes: ...
    def exchange(self, peer_public_key: bytes) -> bytes: ...

class ECDHP384KeyExchange:
    def __init__(self) -> None: ...
    def public_key(self) -> bytes: ...
    def exchange(self, peer_public_key: bytes) -> bytes: ...

class ECDHP521KeyExchange:
    def __init__(self) -> None: ...
    def public_key(self) -> bytes: ...
    def exchange(self, peer_public_key: bytes) -> bytes: ...

class CryptoError(Exception): ...

class KeyType(Enum):
    ECDSA_P256 = 0
    ECDSA_P384 = 1
    ECDSA_P521 = 2
    ED25519 = 3
    DSA = 4
    RSA = 5

class PrivateKeyInfo:
    """
    Load a PEM private key and extract valuable info from it.
    Does two things, provide a DER encoded key and hint
    toward its nature (eg. EC, RSA, DSA, etc...)
    """

    def __init__(self, raw_pem_content: bytes, password: bytes | None) -> None: ...
    def public_bytes(self) -> bytes: ...
    def get_type(self) -> KeyType: ...

class SelfSignedCertificateError(Exception): ...
class InvalidNameCertificateError(Exception): ...
class ExpiredCertificateError(Exception): ...
class UnacceptableCertificateError(Exception): ...
class SignatureError(Exception): ...

class QUICHeaderProtection:
    def __init__(self, key: bytes, algorithm: int) -> None: ...
    def mask(self, sample: bytes) -> bytes: ...
