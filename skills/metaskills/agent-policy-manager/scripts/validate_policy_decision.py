#!/usr/bin/env python3
"""Validate a pinned Agentic OS policy decision record."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
def text(v):return isinstance(v,str) and bool(v.strip())
def validate(d):
 f=[]
 if not isinstance(d,dict):return ["root must be an object"]
 if d.get("schema_version")!=1 or not text(d.get("decision_id")):f.append("schema_version 1 and decision_id required")
 if d.get("decision") not in {"ALLOW","DENY","REQUIRE_APPROVAL"}:f.append("invalid decision")
 for k in ("subject_ref","asset_ref","action","target","environment","data_class","risk_tier","policy_version","run_id","nonce","issued_at","expires_at","audit_id"):
  if not text(d.get(k)):f.append(f"{k} required")
 for k in ("conditions","obligations","approvals"):
  if not isinstance(d.get(k),list):f.append(f"{k} must be an array")
 if d.get("decision")=="REQUIRE_APPROVAL" and not d.get("approvals"):f.append("approval decision requires approvers")
 if d.get("decision")=="ALLOW" and d.get("approval_satisfied") not in {True,False}:f.append("ALLOW requires approval_satisfied boolean")
 if d.get("replayed") is not False:f.append("decision must not be replayed")
 return f
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("decision",type=Path);a=p.parse_args()
 try:d=json.loads(a.decision.read_text())
 except (OSError,json.JSONDecodeError) as e:print(f"ERROR {e}",file=sys.stderr);return 2
 f=validate(d)
 for x in f:print(f"FAIL {x}")
 if f:return 1
 print("PASS policy decision is valid");return 0
if __name__=="__main__":sys.exit(main())
