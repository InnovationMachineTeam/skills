#!/usr/bin/env python3
"""Validate an optimistic Agentic OS registry reconcile plan."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
DECISIONS={"IN_SYNC","MISSING","UNKNOWN","DRIFTED","INCOMPATIBLE","QUARANTINED"}
def text(v):return isinstance(v,str) and bool(v.strip())
def validate(d):
 f=[]
 if not isinstance(d,dict):return ["root must be an object"]
 if d.get("schema_version")!=1 or not text(d.get("plan_id")):f.append("schema_version 1 and plan_id required")
 rev=d.get("expected_revisions",{})
 if not isinstance(rev,dict) or not all(isinstance(rev.get(k),int) and rev[k]>=0 for k in ("registry","bindings")):f.append("expected integer revisions required")
 obs=d.get("observations")
 if not isinstance(obs,list):f.append("observations must be an array");obs=[]
 ids=set()
 for i,o in enumerate(obs):
  if not isinstance(o,dict) or not text(o.get("asset_ref")) or o["asset_ref"] in ids:f.append(f"observations[{i}] invalid or duplicate");continue
  ids.add(o["asset_ref"])
  if o.get("decision") not in DECISIONS:f.append(f"observations[{i}].decision invalid")
  if not isinstance(o.get("evidence"),list) or not o["evidence"]:f.append(f"observations[{i}].evidence required")
 tx=d.get("transaction")
 if not isinstance(tx,dict) or not isinstance(tx.get("operations"),list) or not text(tx.get("rollback")):f.append("transaction operations and rollback required")
 if d.get("authorized") not in {True,False}:f.append("authorized boolean required")
 return f
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("plan",type=Path);a=p.parse_args()
 try:d=json.loads(a.plan.read_text())
 except (OSError,json.JSONDecodeError) as e:print(f"ERROR {e}",file=sys.stderr);return 2
 f=validate(d)
 for x in f:print(f"FAIL {x}")
 if f:return 1
 print("PASS registry reconcile plan is valid");return 0
if __name__=="__main__":sys.exit(main())
