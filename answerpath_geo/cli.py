import argparse
from .core import extract_records, mine, write_outputs

def main():
 p=argparse.ArgumentParser(prog="answerpath", description="Mine user questions for GEO/AEO")
 p.add_argument("topic", help="service, business, website or keyword")
 p.add_argument("--input", action="append", default=[], help="owned JSON/JSONL/CSV export or directory; repeatable")
 p.add_argument("--out", default="answerpath-output")
 p.add_argument("--no-generated", action="store_true", help="only keep observed questions")
 a=p.parse_args(); rows=[]
 for x in a.input: rows.extend(extract_records(x))
 qs=mine(a.topic, rows, not a.no_generated); out=write_outputs(qs,a.out)
 print(f"Wrote {len(qs)} questions to {out} (observed={sum(q.evidence.startswith('observed') for q in qs)})")
