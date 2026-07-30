# Route: build-sync

Build a generated, self-contained distribution artifact from canonical skills.

Use a new staging directory. Reject symlinks and paths escaping the package. Copy the complete contents of each selected skill, preserve category layout, and generate a plugin manifest whose skill paths directly contain skill folders. Emit content hashes and source revision when available.

After building, compare expected and actual inventories and run portable validation. Do not edit the generated bundle manually, promote it, install it, or publish it unless those actions are separately authorized.
