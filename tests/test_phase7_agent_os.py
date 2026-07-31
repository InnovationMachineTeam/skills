#!/usr/bin/env python3
"""End-to-end and adversarial tests for the minimal Agentic OS slice."""
from __future__ import annotations
import copy, importlib.util, json, sys, unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
FIXTURE=ROOT/"tests/fixtures/agent-os-marketplace-release"
def mod(name,rel):
 s=importlib.util.spec_from_file_location(name,ROOT/rel);assert s and s.loader
 m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
ARCH=mod("p7arch","skills/metaskills/agent-os-architect/scripts/validate_architecture.py")
BOOT=mod("p7boot","skills/metaskills/agent-os-bootstrapper/scripts/validate_bootstrap_manifest.py")
REG=mod("p7reg","skills/metaskills/agent-registry-manager/scripts/validate_reconcile_plan.py")
RUN=mod("p7run","skills/metaskills/agent-runtime-manager/scripts/validate_runtime_record.py")
POL=mod("p7pol","skills/metaskills/agent-policy-manager/scripts/validate_policy_decision.py")
OBS=mod("p7obs","skills/metaskills/agent-observer/scripts/validate_trace_bundle.py")
EVAL=mod("p7eval","skills/metaskills/agent-os-evaluator/scripts/validate_release_evidence.py")
def load(name):return json.loads((FIXTURE/name).read_text())

class AgentOsTests(unittest.TestCase):
 def test_complete_walking_skeleton_contract_passes(self):
  validators=[(ARCH,"architecture.json"),(BOOT,"bootstrap-manifest.json"),(REG,"reconcile-plan.json"),(RUN,"runtime-record.json"),(POL,"policy-decision.json"),(OBS,"trace-bundle.json"),(EVAL,"release-evidence.json")]
  for validator,name in validators:self.assertEqual([],validator.validate(load(name)),name)
 def test_unapproved_bootstrap_and_production_activation_fail(self):
  d=load("bootstrap-manifest.json");d["architecture"]["status"]="draft";d["production_activation"]=True;d["credentials"]="production"
  f=BOOT.validate(d);self.assertTrue(any("approved" in x for x in f));self.assertTrue(any("activation" in x for x in f));self.assertTrue(any("synthetic" in x for x in f))
 def test_runtime_false_success_and_policy_replay_fail(self):
  run=load("runtime-record.json");run["artifacts"]=[];run["verification_evidence"]=""
  self.assertTrue(any("success" in x for x in RUN.validate(run)))
  policy=load("policy-decision.json");policy["replayed"]=True
  self.assertTrue(any("replayed" in x for x in POL.validate(policy)))
 def test_registry_stale_contract_and_private_escape_require_external_checks(self):
  d=load("reconcile-plan.json");d["expected_revisions"]["registry"]=-1
  self.assertTrue(any("revisions" in x for x in REG.validate(d)))
  routing=json.loads((ROOT/"skills/metaskills/agent-registry-manager/evals/behavior.json").read_text())
  self.assertTrue(any(c["id"]=="private" for c in routing["cases"]))
 def test_observer_rejects_duplicate_unredacted_events(self):
  d=load("trace-bundle.json");d["events"][1]["event_id"]=d["events"][0]["event_id"];d["events"][1]["redacted"]=False
  f=OBS.validate(d);self.assertTrue(any("duplicate" in x for x in f));self.assertTrue(any("redacted" in x for x in f))
 def test_evaluator_cannot_release_with_blocking_failure(self):
  d=load("release-evidence.json");d["layers"][3]["verdict"]="FAIL"
  self.assertTrue(any("forbids RELEASE" in x for x in EVAL.validate(d)))
 def test_all_agent_os_eval_fixtures_have_positive_and_negative_routes(self):
  names=["agent-os-architect","agent-os-bootstrapper","agent-registry-manager","agent-runtime-manager","agent-policy-manager","agent-observer","agent-os-evaluator"]
  for name in names:
   routing=json.loads((ROOT/f"skills/metaskills/{name}/evals/routing.json").read_text())
   triggers={c["expected_trigger"] for c in routing["cases"]}
   self.assertEqual({True,False},triggers,name)
   behavior=json.loads((ROOT/f"skills/metaskills/{name}/evals/behavior.json").read_text())
   self.assertTrue(all(c.get("expected_properties") and isinstance(c.get("forbidden_properties"),list) for c in behavior["cases"]),name)

if __name__=="__main__":unittest.main()
