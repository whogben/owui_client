import pytest
import sys
import os
import asyncio
import threading
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

# Add the project root to sys.path so we can import 'refs'
# This assumes the file is at owui_client/tests/conftest.py
# Project root (owui_client) is ../
PROJECT_ROOT = Path(__file__).parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

# Also ensure src is in path for the client itself
CLIENT_SRC_ROOT = PROJECT_ROOT / "src"
if str(CLIENT_SRC_ROOT) not in sys.path:
    sys.path.append(str(CLIENT_SRC_ROOT))

try:
    from refs.owui_test_util import OpenWebUITestServer
except ImportError:
    # Fallback or mock if refs not available in some environments, but here it should be.
    print("Warning: Could not import refs.owui_test_util")
    OpenWebUITestServer = None

from owui_client.client import OpenWebUI


@pytest.fixture(scope="session")
def owui_server_session():
    """
    Spins up the Open WebUI server once for the entire test session.
    Returns a dictionary with connection details.
    """
    if not OpenWebUITestServer:
        pytest.skip("OpenWebUITestServer not available")

    # Configure your test server options here
    server = OpenWebUITestServer(branch="main", admin_api_key="sk-test_master_key")

    print("\n[pytest] Starting OWUI Docker container...")
    try:
        # start() is blocking in the util, which is fine for session fixture setup
        port = server.start()
        base_url = f"http://localhost:{port}/api"

        yield {
            "base_url": base_url,
            "api_key": server.admin_api_key,
            "token": server.admin_token,
            "port": port,
        }
    finally:
        print("\n[pytest] Stopping OWUI Docker container...")
        server.stop()


@pytest.fixture
def client(owui_server_session):
    """
    Provides a fresh configured OpenWebUI client for each test function.
    """
    return OpenWebUI(
        api_url=owui_server_session["base_url"],
        api_key=owui_server_session["token"],
    )


class MockOpenAIHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/v1/models":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "object": "list",
                "data": [
                    {
                        "id": "gpt-3.5-turbo",
                        "object": "model",
                        "created": 1677610602,
                        "owned_by": "openai",
                    },
                    {
                        "id": "gpt-4",
                        "object": "model",
                        "created": 1687882411,
                        "owned_by": "openai",
                    },
                ],
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/v1/chat/completions":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            # body = json.loads(post_data)

            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "id": "chatcmpl-123",
                "object": "chat.completion",
                "created": 1677652288,
                "model": "gpt-3.5-turbo",
                "choices": [
                    {
                        "index": 0,
                        "message": {
                            "role": "assistant",
                            "content": "This is a mock response from the test provider.",
                        },
                        "finish_reason": "stop",
                    }
                ],
                "usage": {
                    "prompt_tokens": 9,
                    "completion_tokens": 12,
                    "total_tokens": 21,
                },
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
        elif self.path == "/v1/audio/speech":
            self.send_response(200)
            self.send_header("Content-Type", "audio/mpeg")
            self.end_headers()
            # Return dummy MP3 bytes
            self.wfile.write(b"FAKE_MP3_DATA")
        elif self.path == "/v1/audio/transcriptions":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"text": "This is a mock transcription."}
            self.wfile.write(json.dumps(response).encode("utf-8"))
        elif self.path == "/v1/embeddings":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "object": "list",
                "data": [
                    {"object": "embedding", "embedding": [0.1, 0.2, 0.3], "index": 0}
                ],
                "model": "text-embedding-ada-002",
                "usage": {"prompt_tokens": 5, "total_tokens": 5},
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


@pytest.fixture(scope="session")
def mock_openai_server():
    """
    Starts a mock OpenAI server on a separate thread.
    Returns the base URL (e.g. http://host.docker.internal:PORT/v1)
    """
    # Use port 0 to let OS choose a free port
    server = HTTPServer(("0.0.0.0", 0), MockOpenAIHandler)
    port = server.server_port

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    # IMPORTANT: Since OWUI is running in Docker, it needs to access the host.
    # 'host.docker.internal' works on Docker Desktop for Mac/Windows.
    # For Linux, you might need extra config, but we'll assume standard Docker Desktop dev env.
    base_url = f"http://host.docker.internal:{port}/v1"

    yield base_url

    server.shutdown()


class MockOllamaHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/api/tags":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "models": [
                    {
                        "name": "llama2:latest",
                        "model": "llama2:latest",
                        "modified_at": "2023-11-04T16:28:50.792575724+08:00",
                        "size": 3826793677,
                        "digest": "sha256:mockdigest",
                        "details": {
                            "parent_model": "",
                            "format": "gguf",
                            "family": "llama",
                            "families": ["llama"],
                            "parameter_size": "7B",
                            "quantization_level": "Q4_0",
                        },
                    },
                    {
                        "name": "mistral:latest",
                        "model": "mistral:latest",
                        "modified_at": "2023-11-04T16:28:50.792575724+08:00",
                        "size": 4826793677,
                        "digest": "sha256:mockdigest2",
                        "details": {
                            "parent_model": "",
                            "format": "gguf",
                            "family": "llama",
                            "families": ["llama"],
                            "parameter_size": "7B",
                            "quantization_level": "Q4_0",
                        },
                    },
                ]
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
        elif self.path == "/api/version":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"version": "0.1.14"}).encode("utf-8"))
        elif self.path == "/api/ps":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "models": [
                    {
                        "name": "llama2:latest",
                        "model": "llama2:latest",
                        "size": 3826793677,
                        "digest": "sha256:mockdigest",
                        "details": {
                            "parent_model": "",
                            "format": "gguf",
                            "family": "llama",
                            "families": ["llama"],
                            "parameter_size": "7B",
                            "quantization_level": "Q4_0",
                        },
                        "expires_at": "2023-11-04T17:28:50.792575724+08:00",
                        "size_vram": 3826793677,
                    }
                ]
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/api/chat":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data)
            stream = body.get("stream", True)

            self.send_response(200)
            self.send_header(
                "Content-Type", "application/x-ndjson" if stream else "application/json"
            )
            self.end_headers()

            response_data = {
                "model": body.get("model", "llama2"),
                "created_at": "2023-08-04T19:22:45.499127Z",
                "message": {
                    "role": "assistant",
                    "content": "This is a mock Ollama response.",
                },
                "done": True,
            }

            if stream:
                # Send as a single chunk for simplicity in mock, but follow ndjson format
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
                self.wfile.write(b"\n")
            else:
                self.wfile.write(json.dumps(response_data).encode("utf-8"))

        elif self.path == "/api/generate":
            content_length = int(self.headers["Content-Length"])
            post_data = self.rfile.read(content_length)
            body = json.loads(post_data)
            stream = body.get("stream", True)

            self.send_response(200)
            self.send_header(
                "Content-Type", "application/x-ndjson" if stream else "application/json"
            )
            self.end_headers()

            response_data = {
                "model": body.get("model", "llama2"),
                "created_at": "2023-08-04T19:22:45.499127Z",
                "response": "This is a mock Ollama generation.",
                "done": True,
            }

            if stream:
                self.wfile.write(json.dumps(response_data).encode("utf-8"))
                self.wfile.write(b"\n")
            else:
                self.wfile.write(json.dumps(response_data).encode("utf-8"))

        elif self.path == "/api/show":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "license": "MIT",
                "modelfile": "# Modelfile",
                "parameters": "stop",
                "template": "{{ .Prompt }}",
                "details": {
                    "parent_model": "",
                    "format": "gguf",
                    "family": "llama",
                    "families": ["llama"],
                    "parameter_size": "7B",
                    "quantization_level": "Q4_0",
                },
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif self.path == "/api/embed":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"embeddings": [[0.1, 0.2, 0.3]]}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif self.path == "/api/embeddings":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"embedding": [0.1, 0.2, 0.3]}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(json.dumps({"status": True}).encode("utf-8"))


@pytest.fixture(scope="session")
def mock_ollama_server():
    """
    Starts a mock Ollama server on a separate thread.
    Returns the base URL (e.g. http://host.docker.internal:PORT)
    """
    server = HTTPServer(("0.0.0.0", 0), MockOllamaHandler)
    port = server.server_port

    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()

    base_url = f"http://host.docker.internal:{port}"
    yield base_url

    server.shutdown()
