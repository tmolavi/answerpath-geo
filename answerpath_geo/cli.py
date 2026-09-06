import argparse, sys
from .core import extract_records, mine, write_outputs

def main(argv=None):
    argv=sys.argv[1:] if argv is None else argv
    if argv and argv[0]=="mcp":
        from .mcp import stdio; stdio(); return
    if argv and argv[0] in {"serve-mcp","mcp-http"}:
        from .mcp import http
        p=argparse.ArgumentParser(prog="answerpath serve-mcp"); p.add_argument("--host",default="127.0.0.1"); p.add_argument("--port",type=int,default=8787); a=p.parse_args(argv[1:]); http(a.host,a.port); return
    p=argparse.ArgumentParser(prog="answerpath", description="Mine user questions for GEO/AEO")
    p.add_argument("topic", help="service, business, website or keyword"); p.add_argument("--input", action="append", default=[], help="owned JSON/JSONL/CSV export or directory; repeatable"); p.add_argument("--out", default="answerpath-output"); p.add_argument("--no-generated", action="store_true", help="only keep observed questions")
    a=p.parse_args(argv); rows=[]
    for x in a.input: rows.extend(extract_records(x))
    qs=mine(a.topic, rows, not a.no_generated); out=write_outputs(qs,a.out)
    print(f"Wrote {len(qs)} questions to {out} (observed={sum(q.evidence.startswith('observed') for q in qs)})")
