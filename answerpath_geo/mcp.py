"""Minimal dependency-free MCP-compatible JSON-RPC transports."""
import json, sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from .core import mine

TOOLS = [{"name":"discover_questions","description":"Extract and classify observed questions, then optionally add labeled GEO/AEO hypotheses.","inputSchema":{"type":"object","properties":{"topic":{"type":"string"},"inputs":{"type":"array","items":{"type":"object","properties":{"text":{"type":"string"},"source":{"type":"string"}}}},"include_generated":{"type":"boolean","default":True}},"required":["topic"]}}]

def call_tool(name, args):
    if name != "discover_questions": raise ValueError(f"unknown tool: {name}")
    rows=[(x.get("text",""), x.get("source","mcp")) for x in args.get("inputs",[]) if isinstance(x,dict)]
    result=[q.__dict__ for q in mine(args["topic"], rows, args.get("include_generated",True))]
    return {"content":[{"type":"text","text":json.dumps(result,ensure_ascii=False)}],"structuredContent":{"questions":result}}

def handle(req):
    method=req.get("method"); rid=req.get("id")
    if method=="initialize": result={"protocolVersion":"2024-11-05","capabilities":{"tools":{}},"serverInfo":{"name":"answerpath-geo","version":"0.1.0"}}
    elif method=="tools/list": result={"tools":TOOLS}
    elif method=="tools/call": result=call_tool(req.get("params",{}).get("name"),req.get("params",{}).get("arguments",{}))
    else: return {"jsonrpc":"2.0","id":rid,"error":{"code":-32601,"message":"Method not found"}}
    return {"jsonrpc":"2.0","id":rid,"result":result}

def stdio():
    for line in sys.stdin:
        try: print(json.dumps(handle(json.loads(line)),ensure_ascii=False),flush=True)
        except Exception as e: print(json.dumps({"jsonrpc":"2.0","id":None,"error":{"code":-32000,"message":str(e)}},ensure_ascii=False),flush=True)

class Handler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path.rstrip("/") != "/mcp": self.send_error(404); return
        n=int(self.headers.get("Content-Length","0"));
        try: body=json.loads(self.rfile.read(n)); out=handle(body); raw=json.dumps(out,ensure_ascii=False).encode()
        except Exception as e: raw=json.dumps({"jsonrpc":"2.0","id":None,"error":{"code":-32000,"message":str(e)}},ensure_ascii=False).encode()
        self.send_response(200); self.send_header("Content-Type","application/json"); self.send_header("Content-Length",str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def log_message(self,*args): pass

def http(host="127.0.0.1", port=8787):
    ThreadingHTTPServer((host,port),Handler).serve_forever()
