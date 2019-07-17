"""
ZFS Backup Consistency Agent
"""
import subprocess
import hashlib

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


class File():
    """
    File representation
    """
    def __init__(self, name, filesystem, date_modified=None, crc=None):
        """
        :param name: file path
        :param: date_modified: modification date
        :param: crc: calculated sum
        :param: filesystem: filesystem or snapshot
        """
        self.name = name
        self.date_modified = date_modified
        self.crc = crc
        self.filesystem = filesystem

        self._get_date_modified()

    def __str__(self):
        return f"{self.name}"

    def calculate_crc(buffer_size=4096):
        md5sum = hashlib.md5()
        with open(self.name, "rb") as f:
            for chunk in iter(lambda: f.read(buffer_size), b""):
                md5sum.update(chunk)
        self.crc = md5sum.hexdigest()

    def _get_date_modified():
        self.date_modified = os.path.getmtime(self.name)


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
