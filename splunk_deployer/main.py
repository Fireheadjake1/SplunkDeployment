"""Main entrypoint"""
# Standard libraries
from argparse import ArgumentParser
from pathlib import Path, PurePosixPath

# Third party libraries
from fabric import Connection

# Project libraries
from splunk_deployer.constants import VERSION
from splunk_deployer.openssl_commands import create_csr_cmd,create_ca_cmd, create_key_cmd, sign_csr_cmd

REMOTE_OPENSSL_DIR=PurePosixPath("/opt/splunk/openssl/")
REMOTE_PRIVATE_CERT_KEY=REMOTE_OPENSSL_DIR/"server.pem"

def main():
    parser=ArgumentParser()
    parser.add_argument("--hostname", type=str, required=True, help="desired hostname for the new node")
    parser.add_argument("-ip", type=str, required=True, help="ip of the new node")
    parser.add_argument("-keyfile", "-k", type=Path, required=False, help="Path of the local private ssh key")
    parser.add_argument("-password", "-p", type=str, required=True, help="Password lmao")
    parser.add_argument("-user", "-u", type=str, required=True, help="User lmao")
    args=parser.parse_args()

    with Connection(host=args.ip, user=args.user, port=22, connect_timeout=15, connect_kwargs={"password":args.password}) as conn:
        conn.open()
        #conn.run("whoami", warn=True, hide=True)
        conn.run(create_key_cmd(), warn=True, hide=False)

if __name__ == "__main__":
    main()
	    