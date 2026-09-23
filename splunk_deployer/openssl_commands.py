from pathlib import Path

def create_key_cmd(key_path: Path) -> str:
    return f"openssl genpkey -algorithm RSA -pkeyopt rsa_keygen_bits:2048 -out {key_path}"


def create_ca_cmd(common_name: str, expiration_days: int, key_path: Path, cert_path: Path) -> str:
    return f'openssl req -x509 -new -key {key_path} -sha256 -days {expiration_days} -subj "/CN={common_name}" -addext "basicConstraints=critical,CA:TRUE" -addext "keyUsage=critical,keyCertSign,cRLSign" -out {cert_path}'


def create_csr_cmd(key_path: Path, csr_path: Path, common_name: str) -> str:
    return (
        f'openssl req -new -key {key_path} -out {csr_path} -subj "/C=US/ST=Colorado/L=Denver/O=MyOrg/CN={common_name}"'
    )


def sign_csr_cmd(ca_cert: Path, ca_key: Path, csr_path: Path, server_cert: Path) -> str:
    return f'openssl x509 -req -in {csr_path} -CA {ca_cert} -CAkey {ca_key} -CAcreateserial -days 365 -sha256 -extfile <(printf "basicConstraints=CA:FALSE\nkeyUsage=digitalSignature,keyEncipherment\nextendedKeyUsage=serverAuth") -out {server_cert}'



#stdinput < hostname
#ssh -> hostname
#run bash commands including ssh ones
#move around some Files