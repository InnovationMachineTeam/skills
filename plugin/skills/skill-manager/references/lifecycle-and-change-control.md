# Lifecycle and Change Control

## Contents

- Plan
- Install/update
- Enable/disable
- Retirement
- Verification

## Plan

Every mutation needs exact source, target, current and desired state, consumers, dependencies, validation, rollback, and approval.

## Install/update

Inspect source and provenance, stage outside the active location, validate files and scripts, compare with the current version, run tests, activate through the host mechanism, verify discovery and behavior, and retain last-known-good.

## Enable/disable

Use supported configuration rather than renaming or deleting by convention unless the host explicitly defines that mechanism. Verify actual discovery after the change.

## Retirement

Find consumers, replacements, references, automations, and owners. Prefer disable or quarantine, then migrate, verify, and archive. Permanent deletion is a separate explicit action.

## Verification

Filesystem success is not lifecycle success. Verify host state, routing, functional behavior, dependencies, consumers, and recovery.

