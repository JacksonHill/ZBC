# ZBC
ZFS Backup Consistency

Vision
============

### Agent
Agent is installed on any machine that has configured zfs pool.
Agent performs scans:
1. On current (live) filesystems == last snapshot
2. On previous snapshots mounted somewhere

Each scan consists list of files, their md5 sum, and modification date.
Scans are saved in files, naming convention is the same as
snapshot name - `pool/filesystem@date`.

There's also another file per each scan with the result of
`zfs diff old new | grep -e ^M` with information which files (excluding
directories) has changed from the ZFS point of view.

After each scan is done, it is transferred to the server for further processing.
Agent may be a daemon, or cron script.

### Server
Server is installed on a machine holding primary pool.
Server receives scans from agents, and saves them to the database.
After each scan is saved, consistency checker daemon spins up, and detects
if any file's checksum has changed if file modification date hasn't.

Server runs also a webUI presenting scan reports, consistency reports
and so on.
