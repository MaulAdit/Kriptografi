from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048,
    backend=default_backend()
)
public_key = private_key.public_key()
print("✅ Key pair berhasil dibuat (RSA-2048)\n")

dokumen = b"""
IJAZAH DIGITAL
Nama   : Budi Santoso
NIM    : 2021001234
Prodi  : Teknik Informatika
Nilai  : 3.85
Tanggal: 2025-06-01
"""
print("📄 Dokumen:")
print(dokumen.decode())

signature = private_key.sign(
    dokumen,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print(f"🔏 Signature (hex): {signature.hex()[:64]}...\n")

try:
    public_key.verify(
        signature,
        dokumen,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("✅ VERIFIKASI BERHASIL — Dokumen ASLI dan tidak dimodifikasi!")
except Exception as e:
    print(f"❌ VERIFIKASI GAGAL — Dokumen telah dimodifikasi! ({e})")

dokumen_palsu = dokumen.replace(b"3.85", b"4.00")
print("\n⚠️  Simulasi dokumen dimanipulasi (nilai diubah 3.85 → 4.00):")
try:
    public_key.verify(
        signature,
        dokumen_palsu,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print("✅ Valid")
except Exception:
    print("❌ VERIFIKASI GAGAL — Pemalsuan terdeteksi!")