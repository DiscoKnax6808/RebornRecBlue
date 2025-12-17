from OpenSSL import crypto
import tempfile

def gen_self_signed_cert_files():
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 2048)

    cert = crypto.X509()
    cert.set_version(2)
    cert.set_serial_number(1)

    subject = cert.get_subject()
    subject.commonName = "localhost"

    cert.set_issuer(subject)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(5 * 365 * 24 * 60 * 60)
    cert.set_pubkey(k)
    cert.sign(k, "sha256")

    cert_pem = crypto.dump_certificate(crypto.FILETYPE_PEM, cert)
    key_pem = crypto.dump_privatekey(crypto.FILETYPE_PEM, k)

    cert_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
    key_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")

    cert_file.write(cert_pem)
    key_file.write(key_pem)

    cert_file.close()
    key_file.close()

    return cert_file.name, key_file.name
