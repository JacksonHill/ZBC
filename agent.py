"""
ZFS Backup Consistency Agent
"""
import subprocess


class Snapshot():
    """
    Snapshot representation
    """
    def __init__(self, name, used, avail, refer, mountpoint):
        self.name = name
        self.used = used
        self.avail = avail
        self.refer = refer
        self.mountpoint = mountpoint
        self.date = None

        self._extract_date()

    def __str__(self):
        return f"{self.name}"

    def _extract_date(self):
        if b'@' in self.name:
            self.date = self.name.split(b'@')[1]


def get_filesystems():
    cmd = ['zfs', 'list', '-H']
    res = subprocess.check_output(cmd)
    for line in res.split(b'\n'):
        print(parse_snapshot(line))


def get_snapshots():
    cmd = ['zfs', 'list', '-t', 'snapshot', '-H']
    res = subprocess.check_output(cmd)
    for line in res.split(b'\n'):
        print(parse_snapshot(line))


def parse_snapshot(snapshot_line):
    """
    NAME USED  AVAIL  REFER  MOUNTPOINT
    """
    values = snapshot_line.split(b'\t')
    if len(values) < 4:
        return None
    snapshot = Snapshot(name=values[0],
                        used=values[1],
                        avail=values[2],
                        refer=values[3],
                        mountpoint=values[4])
    return snapshot


get_snapshots()
get_filesystems()
