"""
Utility to spin up an Open WebUI test server with a specific admin user and API key.
Can be used as a library or a standalone script.
"""

import argparse
import os
import subprocess
import sys
import time
import httpx
import socket
from contextlib import contextmanager
from typing import Optional

REPO_URL = "https://github.com/open-webui/open-webui.git"
DOCKER_IMAGE_BASE = "ghcr.io/open-webui/open-webui"
LDAP_IMAGE = "osixia/openldap:latest"


def run_command(cmd, cwd=None, capture_output=False, input=None):
    """Run a shell command."""
    print(f"Running: {' '.join(cmd)}")
    if capture_output:
        result = subprocess.run(
            cmd, cwd=cwd, check=True, capture_output=True, text=True, input=input
        )
        return result.stdout.strip()
    else:
        subprocess.run(
            cmd, cwd=cwd, check=True, input=input, text=True if input else False
        )


def check_docker_running():
    """Check if docker daemon is running."""
    try:
        run_command(["docker", "info"], capture_output=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def checkout_repo(target_dir, branch="main", version=None):
    """Clone or update the repository."""
    if not os.path.exists(target_dir):
        print(f"Cloning into {target_dir}...")
        run_command(["git", "clone", REPO_URL, target_dir])
    else:
        print(f"Updating existing repo in {target_dir}...")
        # Ensure we can fetch
        run_command(["git", "fetch", "--all"], cwd=target_dir)

    if version:
        print(f"Checking out version {version}...")
        run_command(["git", "checkout", version], cwd=target_dir)
    else:
        print(f"Checking out branch {branch}...")
        run_command(["git", "checkout", branch], cwd=target_dir)
        run_command(["git", "pull"], cwd=target_dir)


def get_free_port():
    """Find a free port."""
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def wait_for_port(port, timeout=60):
    """Wait for a TCP port to be open."""
    print(f"Waiting for port {port}...")
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.create_connection(("localhost", port), timeout=1):
                print(f"Port {port} is open.")
                return True
        except (socket.timeout, ConnectionRefusedError, OSError):
            time.sleep(1)
            print(".", end="", flush=True)
    print(f"\nTimeout waiting for port {port}.")
    return False


def wait_for_server(port, timeout=120):
    """Wait for the server to be available."""
    url = f"http://localhost:{port}/health"  # Health endpoint is usually faster/lighter
    # Fallback to checking openapi.json if health isn't available/standard
    openapi_url = f"http://localhost:{port}/openapi.json"

    print(f"Waiting for server at localhost:{port}...")

    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            # Try openapi.json as it's a sure sign the backend is fully up
            response = httpx.get(openapi_url, follow_redirects=True)
            if response.status_code == 200:
                # Verify it's actually JSON content
                content_type = response.headers.get("content-type", "")
                if (
                    "application/json" in content_type
                    or response.text.strip().startswith("{")
                ):
                    print("Server is up and ready.")
                    return True
        except httpx.RequestError:
            pass

        time.sleep(2)
        print(".", end="", flush=True)

    print("\nTimeout waiting for server.")
    return False


def setup_admin_user(port, email, password, container_name) -> Optional[dict]:
    """
    Create the admin user via signup endpoint and generate an API key.
    Returns a dict with 'api_key' and 'token' on success, None on failure.
    """
    base_url = f"http://localhost:{port}"
    print(f"Setting up admin user {email}...")

    # 1. Signup (creates the first user as admin)
    signup_url = f"{base_url}/api/v1/auths/signup"
    payload = {
        "email": email,
        "password": password,
        "name": "Admin User",
        "profile_image_url": "/user.png",
    }

    try:
        response = httpx.post(signup_url, json=payload, follow_redirects=True)
        if response.status_code != 200:
            print(f"Signup failed: {response.status_code} {response.text}")
            # If 403/400, maybe user exists. Try signing in?
            # But this is a fresh container, so it should work unless persistent volume is reused (which we don't do here)
            return None

        data = response.json()
        user_id = data.get("id")
        token = data.get("token")

        if not user_id:
            print("Signup response did not contain user ID.")
            return None

        if not token:
            print("Signup response did not contain token.")
            return None

        print(f"Admin user created with ID: {user_id}")

        # 2. Generate API Key via API
        print(f"Generating API key for user {user_id}...")

        api_key_url = f"{base_url}/api/v1/auths/api_key"
        headers = {"Authorization": f"Bearer {token}"}

        key_response = httpx.post(api_key_url, headers=headers, follow_redirects=True)

        if key_response.status_code != 200:
            print(
                f"Failed to generate API key: {key_response.status_code} {key_response.text}"
            )
            return None

        key_data = key_response.json()
        api_key = key_data.get("api_key")

        if not api_key:
            print("API key response did not contain api_key.")
            return None

        print(f"API key generated successfully: {api_key[:5]}...")
        return {"api_key": api_key, "token": token}

    except Exception as e:
        print(f"Error setting up admin user: {e}")
        return None


class OpenWebUITestServer:
    def __init__(
        self,
        branch="main",
        version=None,
        admin_email="admin@example.com",
        admin_password="password123",
        admin_api_key="test_api_key",
        enable_ldap=False,
    ):
        self.branch = branch
        self.version = version
        self.admin_email = admin_email
        self.admin_password = admin_password
        self.admin_api_key = admin_api_key
        self.admin_token = None
        self.enable_ldap = enable_ldap

        self.container_name = None
        self.ldap_container_name = None
        self.network_name = None
        self.port = None
        self.ldap_port = None

    def start(self):
        # 1. Checkout/Ensure Repo (optional, but good for reference/updating)
        repo_dir = os.path.abspath(
            os.path.join(os.path.dirname(__file__), f"owui_source_{self.branch}")
        )
        try:
            checkout_repo(repo_dir, self.branch, self.version)
        except subprocess.CalledProcessError as e:
            print(f"Warning: Git operations failed: {e}")
            # Continue anyway if possible, we rely on docker image mostly

        # 2. Setup Network if needed
        timestamp = int(time.time())
        if self.enable_ldap:
            self.network_name = f"owui-test-net-{timestamp}"
            print(f"Creating docker network {self.network_name}...")
            run_command(["docker", "network", "create", self.network_name])

        # 3. Start LDAP Container if needed
        ldap_env = []
        if self.enable_ldap:
            self.ldap_port = get_free_port()
            self.ldap_container_name = f"owui-ldap-{timestamp}"
            print(
                f"Starting LDAP container {self.ldap_container_name} on port {self.ldap_port}..."
            )
            run_command(["docker", "pull", LDAP_IMAGE])
            run_command(
                [
                    "docker",
                    "run",
                    "-d",
                    "-p",
                    f"{self.ldap_port}:389",
                    "--name",
                    self.ldap_container_name,
                    "--network",
                    self.network_name,
                    "-e",
                    "LDAP_ORGANISATION=Example Inc.",
                    "-e",
                    "LDAP_DOMAIN=example.org",
                    "-e",
                    "LDAP_ADMIN_PASSWORD=adminpassword",
                    LDAP_IMAGE,
                ]
            )
            # Wait for LDAP to be ready by checking the exposed port
            if not wait_for_port(self.ldap_port, timeout=60):
                self.stop()
                raise Exception("LDAP Server failed to start (port check timeout)")

            # Seed LDAP user
            print("Seeding LDAP user testuser...")
            ldif = """
dn: uid=testuser,dc=example,dc=org
objectClass: inetOrgPerson
uid: testuser
sn: User
cn: Test User
mail: test@example.com
userPassword: password
"""
            try:
                # We might need to wait a bit more for slapd to be fully ready to accept commands
                time.sleep(2)
                run_command(
                    [
                        "docker",
                        "exec",
                        "-i",
                        self.ldap_container_name,
                        "ldapadd",
                        "-x",
                        "-D",
                        "cn=admin,dc=example,dc=org",
                        "-w",
                        "adminpassword",
                    ],
                    input=ldif,
                )
                print("LDAP user seeded.")
            except Exception as e:
                print(f"Failed to seed LDAP user: {e}")
                self.stop()
                raise

            # Configure OWUI to talk to LDAP
            # osixia/openldap defaults:
            # Host: container name (on shared network)
            # Port: 389
            # Admin DN: cn=admin,dc=example,dc=org
            # Password: adminpassword
            ldap_env = [
                "-e",
                "ENABLE_LDAP=true",
                "-e",
                f"LDAP_SERVER_HOST={self.ldap_container_name}",
                "-e",
                "LDAP_SERVER_PORT=389",
                "-e",
                "LDAP_SERVER_LABEL=Test LDAP",
                "-e",
                "LDAP_ATTRIBUTE_FOR_MAIL=mail",
                "-e",
                "LDAP_ATTRIBUTE_FOR_USERNAME=uid",
                "-e",
                "LDAP_SEARCH_BASE=dc=example,dc=org",
                "-e",
                "LDAP_APP_DN=cn=admin,dc=example,dc=org",
                "-e",
                "LDAP_APP_PASSWORD=adminpassword",
                "-e",
                "LDAP_USE_TLS=false",
                "-e",
                "LDAP_VALIDATE_CERT=false",
            ]

        # 4. Start OWUI Container
        self.port = get_free_port()
        self.container_name = f"owui-test-{timestamp}"
        image_tag = self.version if self.version else self.branch
        image = f"{DOCKER_IMAGE_BASE}:{image_tag}"
        print(
            f"Starting docker container {self.container_name} ({image}) on port {self.port}..."
        )

        run_command(["docker", "pull", image])

        docker_cmd = [
            "docker",
            "run",
            "--add-host=host.docker.internal:host-gateway",
            "-d",
            "-p",
            f"{self.port}:8080",
            "-e",
            "ENV=dev",
            "-e",
            "ENABLE_API_KEYS=true",
            "-e",
            "USER_PERMISSIONS_FEATURES_API_KEYS=true",
            "--name",
            self.container_name,
        ]

        if self.network_name:
            docker_cmd.extend(["--network", self.network_name])

        if ldap_env:
            docker_cmd.extend(ldap_env)

        docker_cmd.append(image)

        run_command(docker_cmd)

        # 5. Wait for readiness
        if not wait_for_server(self.port):
            self.stop()
            raise Exception("Server failed to start")

        # 6. Setup Admin User
        auth_data = setup_admin_user(
            self.port,
            self.admin_email,
            self.admin_password,
            self.container_name,
        )

        if not auth_data:
            self.stop()
            raise Exception("Failed to setup admin user")

        self.admin_api_key = auth_data["api_key"]
        self.admin_token = auth_data["token"]

        print(f"\nOpen WebUI Test Server running at: http://localhost:{self.port}")
        print(f"Admin Email: {self.admin_email}")
        print(f"Admin Password: {self.admin_password}")
        print(f"Admin API Key: {self.admin_api_key}")
        print(f"Admin Token: {self.admin_token[:10]}...")
        if self.enable_ldap:
            print(f"LDAP Server running at: localhost:{self.ldap_port}")
            print("LDAP Test User: testuser / password")

        return self.port

    def stop(self):
        if self.container_name:
            print(f"Stopping and removing container {self.container_name}...")
            subprocess.run(
                ["docker", "stop", self.container_name],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["docker", "rm", self.container_name],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.container_name = None

        if self.ldap_container_name:
            print(f"Stopping and removing container {self.ldap_container_name}...")
            subprocess.run(
                ["docker", "stop", self.ldap_container_name],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            subprocess.run(
                ["docker", "rm", self.ldap_container_name],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.ldap_container_name = None

        if self.network_name:
            print(f"Removing network {self.network_name}...")
            subprocess.run(
                ["docker", "network", "rm", self.network_name],
                check=False,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            self.network_name = None


@contextmanager
def run_test_server(
    branch="main",
    version=None,
    admin_email="admin@example.com",
    admin_password="password123",
    admin_api_key="test_api_key",
    enable_ldap=False,
):
    server = OpenWebUITestServer(
        branch,
        version,
        admin_email,
        admin_password,
        admin_api_key,
        enable_ldap=enable_ldap,
    )
    try:
        port = server.start()
        yield server
    finally:
        server.stop()


def main():
    parser = argparse.ArgumentParser(description="Run Open WebUI Test Server.")
    parser.add_argument(
        "-branch", default="main", help="Branch/Image tag to use (default: main)"
    )
    parser.add_argument("-version", help="Specific version tag (optional)")
    parser.add_argument("-email", default="admin@example.com", help="Admin email")
    parser.add_argument("-password", default="password123", help="Admin password")
    parser.add_argument("-api-key", default="test_api_key", help="Admin API key")
    parser.add_argument(
        "-enable-ldap", action="store_true", help="Enable LDAP test container"
    )
    parser.add_argument(
        "-keep-alive", action="store_true", help="Keep server running until Ctrl+C"
    )

    args = parser.parse_args()

    if not check_docker_running():
        print("Error: Docker is not running.")
        sys.exit(1)

    server = OpenWebUITestServer(
        args.branch,
        args.version,
        args.email,
        args.password,
        args.api_key,
        enable_ldap=args.enable_ldap,
    )
    try:
        server.start()

        if args.keep_alive:
            print("Press Ctrl+C to stop the server...")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping server...")
        else:
            # For testing the utility itself (as requested by user), we might want to keep it alive briefly or just exit
            # The user asked to "make sure it works... by spinning it up and using your browser tool"
            # So if I run this script, I should probably wait for input or keep it alive.
            # But the prompt implies I will do the browsing.

            # If this script is run directly, we probably want it to hang around.
            print("Server is running. Press Ctrl+C to stop.")
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\nStopping server...")

    finally:
        server.stop()


if __name__ == "__main__":
    main()
