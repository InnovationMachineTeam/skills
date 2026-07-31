#!/usr/bin/env python3
"""Validate a reviewable Agentic OS architecture candidate."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

PLANES={"experience","control","execution","knowledge","assurance","operations"}
def text(v): return isinstance(v,str) and bool(v.strip())
def validate(d):
 f=[]
 if not isinstance(d,dict): return ["root must be an object"]
 if d.get("schema_version")!=1 or not text(d.get("id")): f.append("schema_version 1 and id are required")
 if d.get("decision") not in {"JUSTIFIED","SIMPLER_WORKFLOW","RESEARCH_REQUIRED","REJECT"}: f.append("invalid decision")
 for k in ("bounded_use_case","accountable_owner","walking_skeleton","rollback","retirement"):
  if not text(d.get(k)): f.append(f"{k} is required")
 planes=d.get("planes")
 if not isinstance(planes,list): return f+["planes must be an array"]
 seen=set()
 for i,p in enumerate(planes):
  if not isinstance(p,dict) or p.get("name") not in PLANES: f.append(f"planes[{i}] invalid"); continue
  seen.add(p["name"])
  for k in ("owner","source_of_truth","slo","lifecycle"):
   if not text(p.get(k)): f.append(f"planes[{i}].{k} is required")
  for k in ("apis","permissions","threats","failures"):
   if not isinstance(p.get(k),list): f.append(f"planes[{i}].{k} must be an array")
 if seen!=PLANES: f.append(f"missing planes {sorted(PLANES-seen)}")
 if not isinstance(d.get("flows"),list) or not d["flows"]: f.append("flows must be non-empty")
 if not isinstance(d.get("exit_gates"),list) or not d["exit_gates"]: f.append("exit_gates must be non-empty")
 if not isinstance(d.get("rejected_complexity"),list): f.append("rejected_complexity must be an array")
 return f
def main():
 p=argparse.ArgumentParser(description=__doc__); p.add_argument("architecture",type=Path); a=p.parse_args()
 try: d=json.loads(a.architecture.read_text())
 except (OSError,json.JSONDecodeError) as e: print(f"ERROR {e}",file=sys.stderr); return 2
 f=validate(d)
 for x in f: print(f"FAIL {x}")
 if f:return 1
 print("PASS Agentic OS architecture is structurally valid"); return 0
if __name__=="__main__": sys.exit(main())
