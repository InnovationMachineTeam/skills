#!/usr/bin/env python3
"""Validate a redacted Agentic OS trace bundle."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
def text(v):return isinstance(v,str) and bool(v.strip())
def validate(d):
 f=[]
 if not isinstance(d,dict):return ["root must be an object"]
 if d.get("schema_version")!=1 or not text(d.get("trace_id")):f.append("schema_version 1 and trace_id required")
 if not text(d.get("run_id")) or not text(d.get("task_id")):f.append("run_id and task_id required")
 events=d.get("events")
 if not isinstance(events,list) or not events:return f+["events must be non-empty"]
 ids=set();seq=[]
 for i,e in enumerate(events):
  if not isinstance(e,dict):f.append(f"events[{i}] invalid");continue
  if not text(e.get("event_id")) or e["event_id"] in ids:f.append(f"events[{i}] invalid or duplicate")
  else:ids.add(e["event_id"])
  for k in ("type","timestamp","producer","data_class"):
   if not text(e.get(k)):f.append(f"events[{i}].{k} required")
  if e.get("redacted") is not True:f.append(f"events[{i}] must be redacted")
  if not isinstance(e.get("sequence"),int):f.append(f"events[{i}].sequence required")
  else:seq.append(e["sequence"])
  if not isinstance(e.get("versions"),dict) or not e["versions"]:f.append(f"events[{i}].versions required")
 if len(seq)!=len(set(seq)):f.append("duplicate sequence numbers")
 alerts=d.get("alerts",[])
 if not isinstance(alerts,list):f.append("alerts must be an array")
 for i,a in enumerate(alerts):
  if not isinstance(a,dict) or not all(text(a.get(k)) for k in ("severity","owner","runbook_ref","dedupe_key")):f.append(f"alerts[{i}] incomplete")
 return f
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("bundle",type=Path);a=p.parse_args()
 try:d=json.loads(a.bundle.read_text())
 except (OSError,json.JSONDecodeError) as e:print(f"ERROR {e}",file=sys.stderr);return 2
 f=validate(d)
 for x in f:print(f"FAIL {x}")
 if f:return 1
 print("PASS trace bundle is valid");return 0
if __name__=="__main__":sys.exit(main())
