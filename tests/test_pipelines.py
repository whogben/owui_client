import pytest
import threading
import json
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from owui_client.models.openai import OpenAIConfigForm
from owui_client.models.pipelines import AddPipelineForm, DeletePipelineForm

class MockPipelineHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # The backend calls /models to discover if it's a pipeline server (checking for "pipelines" key)
        if self.path.endswith("/models"): 
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "object": "list",
                "data": [
                    {"id": "pipeline-model", "object": "model", "created": 123, "owned_by": "me"}
                ],
                "pipelines": True # Key indicator used by OWUI backend
            }
            self.wfile.write(json.dumps(response).encode("utf-8"))
        
        elif self.path == "/pipelines":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {"data": [{"id": "test-pipeline", "name": "Test Pipeline", "valves": {}, "url": "http://example.com"}]}
            self.wfile.write(json.dumps(response).encode("utf-8"))

        elif "/valves/spec" in self.path:
             self.send_response(200)
             self.send_header("Content-Type", "application/json")
             self.end_headers()
             self.wfile.write(json.dumps({"spec": {}}).encode("utf-8"))

        elif "/valves" in self.path: # Matches /pipelines/{id}/valves
             self.send_response(200)
             self.send_header("Content-Type", "application/json")
             self.end_headers()
             self.wfile.write(json.dumps({"valves": {}}).encode("utf-8"))
             
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/pipelines/upload":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"id": "uploaded-pipeline", "name": "Uploaded Pipeline"}).encode("utf-8"))
            
        elif self.path == "/pipelines/add":
            length = int(self.headers.get('content-length', 0))
            data = json.loads(self.rfile.read(length))
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"id": "added-pipeline", "url": data.get("url")}).encode("utf-8"))
            
        elif "/valves/update" in self.path:
             self.send_response(200)
             self.send_header("Content-Type", "application/json")
             self.end_headers()
             self.wfile.write(json.dumps({"status": "updated"}).encode("utf-8"))

        else:
            self.send_response(404)
            self.end_headers()
            
    def do_DELETE(self):
        if self.path == "/pipelines/delete":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "deleted"}).encode("utf-8"))
        else:
            self.send_response(404)
            self.end_headers()


@pytest.fixture
def mock_pipeline_server():
    server = HTTPServer(("0.0.0.0", 0), MockPipelineHandler)
    port = server.server_port
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    
    # IMPORTANT: Since OWUI is running in Docker, it needs to access the host.
    # 'host.docker.internal' works on Docker Desktop for Mac/Windows.
    base_url = f"http://host.docker.internal:{port}"
    
    yield base_url
    
    server.shutdown()


@pytest.mark.asyncio
async def test_pipelines_discovery(client, mock_pipeline_server):
    # Configure OWUI to use the mock pipeline server
    new_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_pipeline_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}}
    )
    await client.openai.update_config(new_config)
    
    # List pipelines
    res = await client.pipelines.list()
    assert "data" in res
    
    # Should find our server. 
    # Note: Since we updated config, it might be at index 0.
    found = False
    for item in res["data"]:
        # The backend returns urls that matched.
        if item["url"] == mock_pipeline_server:
            found = True
            break
    assert found


@pytest.mark.asyncio
async def test_pipeline_operations(client, mock_pipeline_server, tmp_path):
    # Configure first
    new_config = OpenAIConfigForm(
        ENABLE_OPENAI_API=True,
        OPENAI_API_BASE_URLS=[mock_pipeline_server],
        OPENAI_API_KEYS=["sk-mock-key"],
        OPENAI_API_CONFIGS={"0": {"enable": True}}
    )
    await client.openai.update_config(new_config)
    
    # We need to find the index of our mock server. 
    # Since we just set it as the only URL, it should be 0.
    url_idx = 0
    
    # 1. Upload
    # Create a dummy python file
    d = tmp_path / "subdir"
    d.mkdir()
    p = d / "test_pipeline.py"
    p.write_text("print('hello')")
    
    res = await client.pipelines.upload(str(p), url_idx=url_idx)
    assert res["id"] == "uploaded-pipeline"
    
    # 2. Add
    form = AddPipelineForm(url="http://example.com/pipeline.py", urlIdx=url_idx)
    res = await client.pipelines.add(form)
    assert res["id"] == "added-pipeline"
    
    # 3. Get Pipelines
    res = await client.pipelines.get(url_idx=url_idx)
    assert "data" in res
    assert res["data"][0]["id"] == "test-pipeline"
    
    # 4. Valves
    res = await client.pipelines.get_valves("test-pipeline", url_idx=url_idx)
    assert "valves" in res
    
    res = await client.pipelines.get_valves_spec("test-pipeline", url_idx=url_idx)
    assert "spec" in res
    
    res = await client.pipelines.update_valves("test-pipeline", {"param": "value"}, url_idx=url_idx)
    assert res["status"] == "updated"

    # 5. Delete
    form = DeletePipelineForm(id="test-pipeline", urlIdx=url_idx)
    res = await client.pipelines.delete(form)
    assert res["status"] == "deleted"

