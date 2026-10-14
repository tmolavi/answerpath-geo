"""Dependency-free MCP-compatible JSON-RPC transports for AnswerPath GEO."""
from __future__ import annotations
import json
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .core import mine

TOOLS = [
    {
        "name": "discover_questions",
        "description": "Mine authentic user conversational, voice, and multimodal questions asked to AI search engines for a service, website, or keyword.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "topic": {
                    "type": "string",
                    "description": "Business topic, keyword, or service description."
                },
                "url": {
                    "type": "string",
                    "description": "Optional website URL to extract brand, entity, and offering signals from."
                },
                "modality": {
                    "type": "string",
                    "enum": ["all", "text", "voice", "multimodal_image"],
                    "default": "all",
                    "description": "Target query modality: text (conversational), voice (dictation), or multimodal_image (screenshot/image query)."
                },
                "lang": {
                    "type": "string",
                    "enum": ["auto", "fa", "en", "tr", "ar"],
                    "default": "auto",
                    "description": "Target language for prompt generation."
                },
                "count": {
                    "type": "integer",
                    "default": 30,
                    "description": "Number of questions to discover and simulate."
                },
                "inputs": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "text": {"type": "string"},
                            "source": {"type": "string"}
                        }
                    },
                    "description": "Optional observed user query logs."
                },
                "include_generated": {
                    "type": "boolean",
                    "default": True,
                    "description": "Whether to include realistic AI search simulations."
                },
                "benchmark_format": {
                    "type": "boolean",
                    "default": False,
                    "description": "Whether to return in GEO-Scope benchmark schema."
                }
            },
            "required": ["topic"]
        }
    }
]

def call_tool(name: str, args: dict):
    if name != "discover_questions":
        raise ValueError(f"unknown tool: {name}")

    rows = [(x.get("text", ""), x.get("source", "mcp")) for x in args.get("inputs", []) if isinstance(x, dict)]
    benchmark_format = args.get("benchmark_format", False)

    result = mine(
        topic=args.get("topic", ""),
        inputs=rows,
        include_generated=args.get("include_generated", True),
        url=args.get("url"),
        modalities=args.get("modality", "all"),
        lang=args.get("lang", "auto"),
        count=args.get("count", 30),
        benchmark_format=benchmark_format
    )

    if not benchmark_format:
        serializable = [q.to_dict() if hasattr(q, "to_dict") else q.__dict__ for q in result]
    else:
        serializable = result

    return {
        "content": [{"type": "text", "text": json.dumps(serializable, ensure_ascii=False, indent=2)}],
        "structuredContent": {"questions": serializable}
    }

def handle(req: dict) -> dict:
    method = req.get("method")
    rid = req.get("id")

    if method == "initialize":
        result = {
            "protocolVersion": "2024-11-05",
            "capabilities": {"tools": {}},
            "serverInfo": {"name": "answerpath-geo", "version": "0.2.0"}
        }
    elif method == "tools/list":
        result = {"tools": TOOLS}
    elif method == "tools/call":
        result = call_tool(req.get("params", {}).get("name"), req.get("params", {}).get("arguments", {}))
    else:
        return {"jsonrpc": "2.0", "id": rid, "error": {"code": -32601, "message": "Method not found"}}

    return {"jsonrpc": "2.0", "id": rid, "result": result}

def stdio():
    for line in sys.stdin:
        try:
            print(json.dumps(handle(json.loads(line)), ensure_ascii=False), flush=True)
        except Exception as e:
            print(json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}, ensure_ascii=False), flush=True)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path.rstrip("/") != "/mcp":
            self.send_error(404)
            return
        n = int(self.headers.get("Content-Length", "0"))
        try:
            body = json.loads(self.rfile.read(n))
            out = handle(body)
            raw = json.dumps(out, ensure_ascii=False).encode()
        except Exception as e:
            raw = json.dumps({"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(raw)))
        self.end_headers()
        self.wfile.write(raw)

    def log_message(self, *args):
        pass

def http(host="127.0.0.1", port=8787):
    ThreadingHTTPServer((host, port), Handler).serve_forever()
