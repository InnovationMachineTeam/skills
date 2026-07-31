#!/usr/bin/env python3
"""Validate layered Agentic OS release evidence."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path
LAYERS={"architecture","compatibility","registry","policy","runtime","knowledge","observability","operations","security","lifecycle","e2e"}
VERDICTS={"PASS","FAIL","INCONCLUSIVE","WAIVED"};SHA=re.compile(r"^sha256:[0-9a-f]{64}$")
def text(v):return isinstance(v,str) and bool(v.strip())
def validate(d):
 f=[]
 if not isinstance(d,dict):return ["root must be an object"]
 if d.get("schema_version")!=1 or not text(d.get("evaluation_id")):f.append("schema_version 1 and evaluation_id required")
 if not SHA.fullmatch(str(d.get("candidate_hash",""))):f.append("candidate_hash required")
 if not isinstance(d.get("environment"),dict) or not d["environment"]:f.append("environment required")
 layers=d.get("layers")
 if not isinstance(layers,list):return f+["layers must be an array"]
 seen=set();blocking_failure=False
 for i,l in enumerate(layers):
  if not isinstance(l,dict) or l.get("name") not in LAYERS:f.append(f"layers[{i}] invalid");continue
  seen.add(l["name"])
  if l.get("verdict") not in VERDICTS:f.append(f"layers[{i}].verdict invalid")
  if l.get("blocking") not in {True,False}:f.append(f"layers[{i}].blocking required")
  if not isinstance(l.get("evidence_refs"),list) or not l["evidence_refs"]:f.append(f"layers[{i}].evidence_refs required")
  if l.get("blocking") and l.get("verdict") in {"FAIL","INCONCLUSIVE"}:blocking_failure=True
 if seen!=LAYERS:f.append(f"missing layers {sorted(LAYERS-seen)}")
 rec=d.get("recommendation")
 if rec not in {"RELEASE","CONDITIONAL","BLOCK","INCONCLUSIVE"}:f.append("invalid recommendation")
 if blocking_failure and rec=="RELEASE":f.append("blocking failure forbids RELEASE")
 if not isinstance(d.get("raw_evidence"),list) or not d["raw_evidence"]:f.append("raw_evidence required")
 return f
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("evidence",type=Path);a=p.parse_args()
 try:d=json.loads(a.evidence.read_text())
 except (OSError,json.JSONDecodeError) as e:print(f"ERROR {e}",file=sys.stderr);return 2
 f=validate(d)
 for x in f:print(f"FAIL {x}")
 if f:return 1
 print("PASS Agentic OS release evidence is valid");return 0
if __name__=="__main__":sys.exit(main())
