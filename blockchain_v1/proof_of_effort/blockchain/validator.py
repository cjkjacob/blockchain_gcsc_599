from ecdsa import VerifyingKey, SECP256k1, BadSignatureError
from ecdsa.util import sigdecode_string
import hashlib, json

class EffortValidator:
    def __init__(self, min_score=10):
        self.min_score = min_score

    def is_valid(self, effort_data, validated_by):
        if not effort_data.get("effort_score") or effort_data["effort_score"] < self.min_score:
            return False
        if not effort_data.get("submission") or not effort_data["submission"].get("file_url"):
            return False
        if not validated_by:
            return False
        return True

def verify_proof(effort_data, signature_hex, public_key_hex, debug=False):
    try:
        canonical = json.dumps(effort_data, sort_keys=True, separators=(',', ':'))
        digest = hashlib.sha256(canonical.encode()).digest()
        print("backend digest", digest.hex())

        pubkey_bytes = bytes.fromhex(public_key_hex)
        # verifying_key = VerifyingKey.from_string(pubkey_bytes[1:], curve=SECP256k1)  # Remove 04
        verifying_key = VerifyingKey.from_string(bytes.fromhex(public_key_hex), curve=SECP256k1)
        signature_bytes = bytes.fromhex(signature_hex)
        print("DEBUG verify_proof:")
        print("  Digest:", digest.hex())
        print("  Signature hex:", signature_hex)
        print("  Signature bytes length:", len(signature_bytes))
        print("  Public key hex:", public_key_hex)
        print("  Public key bytes length:", len(bytes.fromhex(public_key_hex)))

        print(f"PK length: {len(pubkey_bytes)}, raw PK: {pubkey_bytes.hex()}")
        print("Sig r:", signature_bytes[:32].hex())
        print("Sig s:", signature_bytes[32:].hex())

        # Verify raw signature
        valid = verifying_key.verify_digest(signature_bytes, digest, sigdecode=sigdecode_string)
        return valid

    except BadSignatureError as e:
        if debug:
            return {
                "valid": False,
                "error": "BadSignatureError",
                "message": str(e),
                "digest": digest.hex(),
                "canonical_payload": canonical,
                "public_key": public_key_hex,
                "signature": signature_hex
            }
        return False

    except Exception as e:
        if debug:
            return {
                "valid": False,
                "error": "Exception",
                "message": str(e),
                "public_key": public_key_hex,
                "signature": signature_hex
            }
        return False