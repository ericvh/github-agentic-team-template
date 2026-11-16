# Iteration storage contract

This repository contains a pinned copy of the shared iteration archiver. Its
content hashes are in `.iteration-archive-hook.json`; update through the
installer, which refuses edited files and instruction collisions. Installation
does not configure a destination or release any run.

## Before an iteration and on resume

1. Read the experiment ledger or active work-slice issue. Name the current run,
   qualified baseline, next-run inputs, review evidence and rollback holds.
2. Use the host's private storage policy through `ITERATION_ARCHIVE_CONFIG`, or
   the ignored `.local/iteration-archive.json`. The policy, holds and receipts
   must stay outside published source/evidence bundles. Do not invent a missing
   destination or treat a plain directory as a mounted archive.
3. Run `python3 scripts/iteration-archive.py status`. With an already authorized
   `archive` policy, run `resume --execute` for eligible pending work and existing
   mounts. Inspect every held result. An interrupted inventory or image creation
   may require inspection; never remove its transaction state to force progress.
4. Run `preflight --required-bytes N`, where N is the estimated peak scratch
   allocation for the next iteration. A failed gate prevents that space-heavy
   run; preserve its scientific/issue state and report the storage blocker.

## After results are saved

Register a JSON record with `register /private/path/run.json`. It identifies
`schema: 1`, `project`, `iteration`, the exact `source` directory, `execution`
(`active` or `closed`), boolean `released`, explicit `dependencies`, scientific
`result`, `classification`, and a durable `evidence` reference. Use lowercase
project/iteration IDs. The returned run key is `project--iteration`.

Register active runs with `released: false`; update their record after results
and the scientific decision are durable. A closed invalid, failed or inconclusive
run remains evidence. Release only when no current, queued, baseline, review or
rollback consumer needs its writable local files. Update the shared host hold
registry under the same host storage lock; never clear another project's hold.
All policies on a host must use the same local state directory and hold registry.

Run `plan RUN_KEY` and inspect the exact registered root. With standing archive
authority and a configured `archive` mode, run `closeout RUN_KEY --execute` after
each eligible iteration. This is an agent-invoked closeout step, not a daemon.
No further per-run permission is needed within that standing policy. A `plan`
policy never retires evidence even when `--execute` is supplied.

Preserve held records and inspect nonzero exits and per-run `held` results. Do
not convert storage failure into a failed scientific hypothesis or a completed
engineering slice. Repeat closeout after review or dependency release when those
were the hold; a merge is not required for independently released experiment
scratch. Checkpoint storage state in the normal handoff before another run.

## Access and recovery

Completed original paths link into read-only archive images. After mounting the
configured NFS share, `resume --execute` verifies and reattaches the images.
Do not run mutable experiments inside archive mounts. Use
`restore RUN_KEY /new/local/directory` for a verified writable copy; an existing
destination is refused. The original archived result remains unchanged.

The current adapter is macOS APFS via `hdiutil`, with Python 3.10+, `lsof`, `ps`,
`mount`, and `ditto`. Other hosts retain local originals until an adapter is
qualified. Only ordinary directory roots with internal relative links are
eligible. Worktrees, `.private` paths, external/absolute/dangling links,
unsupported filesystem objects and hardlinks outside the run are held.

No generated-cache deletion, NAS expiration, scheduler or service is installed.
File contents, exact paths, hardlinks, symlinks and applicable metadata are
verified. Any explicitly configured GID mapping is reported; macOS provenance,
birthtime, ctime, inode numbers and physical allocation are not restoration
guarantees. Full inventories, image hashes and recovery receipts remain in the
private local state and beside each archive. A failed copy/check leaves local
evidence intact; a journaled cutover can finish retirement after interruption.
