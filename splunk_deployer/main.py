"""Main entrypoint"""
# Standard libraries
import subprocess
from argparse import ArgumentParser
from pathlib import Path, PurePosixPath

# Third party libraries
from fabric import Connection, Config

# Project libraries
from splunk_deployer.constants import VERSION
from splunk_deployer.openssl_commands import create_csr_cmd,create_ca_cmd, create_key_cmd, sign_csr_cmd, create_hostname_cmd

REMOTE_OPENSSL_DIR=PurePosixPath("/opt/splunk/openssl/")
REMOTE_CSR=REMOTE_OPENSSL_DIR/"server.csr"
REMOTE_PRIVATE_CERT_KEY=REMOTE_OPENSSL_DIR/"server.key"
REMOTE_SERVER_CERT=REMOTE_OPENSSL_DIR/"server.pem"
LOCAL_DIR=PurePosixPath("/root/")
LOCAL_CSR=LOCAL_DIR/"server.csr"
LOCAL_PRIVATE_CERT_KEY=LOCAL_DIR/"server.key"
LOCAL_SERVER_CERT=LOCAL_DIR/"server.pem"
CA_CERT=LOCAL_DIR/"ca.crt"
CA_KEY=LOCAL_DIR/"ca.key"


def main():
    parser=ArgumentParser()
    parser.add_argument("--hostname", type=str, required=True, help="desired hostname for the new node")
    parser.add_argument("-ip", type=str, required=True, help="ip of the new node")
    parser.add_argument("-keyfile", "-k", type=Path, required=False, help="Path of the local private ssh key")
    parser.add_argument("-password", "-p", type=str, required=True, help="Password of target user")
    parser.add_argument("-user", "-u", type=str, required=True, help="Username of target user")
    args=parser.parse_args()

    with Connection(host=args.ip, user=args.user, port=22, config=Config(overrides={"sudo":{"password":args.password}}), connect_timeout=15, connect_kwargs={"password":args.password}) as conn:
        conn.open()
        #conn.run("whoami", warn=True, hide=True)
        conn.run(create_key_cmd(REMOTE_PRIVATE_CERT_KEY), warn=True, hide=False)
        conn.sudo(create_hostname_cmd(args.hostname, args.password), warn=True, hide=False)
        conn.run(create_csr_cmd(REMOTE_PRIVATE_CERT_KEY, REMOTE_CSR, args.hostname), warn=True, hide=False)
        conn.get(str(REMOTE_CSR), local=str(LOCAL_CSR), preserve_mode=True)
        conn.get(str(REMOTE_PRIVATE_CERT_KEY), local=str(LOCAL_PRIVATE_CERT_KEY), preserve_mode=True)
        subprocess.run(sign_csr_cmd(CA_CERT, CA_KEY, LOCAL_CSR, LOCAL_SERVER_CERT), check = True, shell = True, capture_output = True)
        conn.put(str(LOCAL_SERVER_CERT), remote=str(REMOTE_SERVER_CERT), preserve_mode=False)

if __name__ == "__main__":
    main()
	    