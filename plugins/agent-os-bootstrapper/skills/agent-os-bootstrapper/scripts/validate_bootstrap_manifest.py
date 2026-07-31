#!/usr/bin/env python3
"""Validate an Agentic OS walking-skeleton bootstrap manifest."""
from __future__ import annotations
import argparse,json,re,sys
from pathlib import Path,PurePosixPath
SHA=re.compile(r"^sha256:[0-9a-f]{64}$")
def text(v):return isinstance(v,str) and bool(v.strip())
def safe(v):
 if not text(v):return False
 p=PurePosixPath(v);return not p.is_absolute() and ".." not in p.parts
def validate(d):
 f=[]
 if not isinstance(d,dict):return ["root must be an object"]
 if d.get("schema_version")!=1 or not text(d.get("bootstrap_id")):f.append("schema_version 1 and bootstrap_id required")
 a=d.get("architecture",{})
 if not isinstance(a,dict) or a.get("status")!="approved" or not text(a.get("id")) or not SHA.fullmatch(str(a.get("hash",""))):f.append("approved architecture id and hash required")
 if not safe(d.get("destination")):f.append("safe relative destination required")
 if d.get("production_activation") is not False:f.append("production_activation must be false")
 if d.get("credentials")!="synthetic":f.append("credentials must be synthetic")
 ops=d.get("operations")
 if not isinstance(ops,list) or not ops:f.append("operations must be non-empty");ops=[]
 paths=set()
 for i,o in enumerate(ops):
  if not isinstance(o,dict) or o.get("action") not in {"create","migrate","generate","validate"}:f.append(f"operations[{i}] invalid");continue
  p=o.get("path")
  if not safe(p) or p in paths:f.append(f"operations[{i}].path unsafe or duplicate")
  paths.add(p)
 for k in ("health_checks","smoke_tests","failure_tests"):
  if not isinstance(d.get(k),list) or not d[k]:f.append(f"{k} must be non-empty")
 if not isinstance(d.get("rollback"),dict) or not text(d["rollback"].get("procedure")):f.append("rollback procedure required")
 return f
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument("manifest",type=Path);a=p.parse_args()
 try:d=json.loads(a.manifest.read_text())
 except (OSError,json.JSONDecodeError) as e:print(f"ERROR {e}",file=sys.stderr);return 2
 f=validate(d)
 for x in f:print(f"FAIL {x}")
 if f:return 1
 print("PASS Agentic OS bootstrap manifest is valid");return 0
if __name__=="__main__":sys.exit(main())
