#!/usr/bin/env python3
"""Validate a durable Agentic OS runtime record."""
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
STATES={"QUEUED","LEASED","RUNNING","WAITING_APPROVAL","VERIFYING","SUCCEEDED","PARTIAL","FAILED","CANCELLED","COMPENSATING","ROLLED_BACK","DEAD_LETTER"}
TERMINAL={"SUCCEEDED","FAILED","CANCELLED","ROLLED_BACK","DEAD_LETTER"}
def text(v):return isinstance(v,str) and bool(v.strip())
def validate(d):
 f=[]
 if not isinstance(d,dict):return ["root must be an object"]
 if d.get("schema_version")!=1 or not text(d.get("run_id")):f.append("schema_version 1 and run_id required")
 if d.get("state") not in STATES:f.append("invalid state")
 for k in ("task_id","idempotency_key","deadline","policy_decision_ref","verifier_ref"):
  if not text(d.get(k)):f.append(f"{k} required")
 pins=d.get("pinned_versions",{})
 if not isinstance(pins,dict) or not all(text(pins.get(k)) for k in ("agent","workflow","model","policy")):f.append("all pinned versions required")
 b=d.get("budgets",{})
 if not isinstance(b,dict) or not all(isinstance(b.get(k),int) and b[k]>=0 for k in ("max_attempts","max_steps")):f.append("non-negative budgets required")
 lease=d.get("lease")
 if d.get("state") in {"LEASED","RUNNING","VERIFYING"} and (not isinstance(lease,dict) or not all(text(lease.get(k)) for k in ("owner","expires_at","fencing_token"))):f.append("active state requires complete lease")
 if not isinstance(d.get("events"),list) or not d["events"]:f.append("events must be non-empty")
 if d.get("state")=="SUCCEEDED" and (not d.get("artifacts") or not text(d.get("verification_evidence"))):f.append("success requires artifacts and verification evidence")
 if d.get("state") not in TERMINAL and not text(d.get("checkpoint_ref")):f.append("non-terminal state requires checkpoint_ref")
 return f
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("record",type=Path);a=p.parse_args()
 try:d=json.loads(a.record.read_text())
 except (OSError,json.JSONDecodeError) as e:print(f"ERROR {e}",file=sys.stderr);return 2
 f=validate(d)
 for x in f:print(f"FAIL {x}")
 if f:return 1
 print("PASS runtime record is valid");return 0
if __name__=="__main__":sys.exit(main())
