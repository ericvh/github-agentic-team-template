#!/usr/bin/env python3
"""Verified per-iteration archival. No age-based deletion or implicit discovery."""
import argparse
import contextlib
import fcntl
import gzip
import hashlib
import json
import os
from pathlib import Path
import plistlib
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import time


class Held(RuntimeError):
    """A preservation gate is not satisfied; retain the local evidence."""


def require(ok, reason):
    if not ok:
        raise Held(reason)


def digest(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(4 * 1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def write_json(path, value):
    """Replace a private receipt durably; never follow a receipt symlink."""
    require(not path.is_symlink(), 'receipt is a symlink')
    fd, name = tempfile.mkstemp(prefix=path.name + '.write-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w') as f:
            json.dump(value, f, indent=2)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(name, path)
        sync_dir(path.parent)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def canonical(path, *, missing=False):
    p = Path(path)
    require(p.is_absolute() and '..' not in p.parts, 'absolute normalized path required')
    require(p.resolve(strict=not missing) == p, 'symlink or noncanonical path: ' + str(p))
    return p


def overlap(a, b):
    return a == b or a.is_relative_to(b) or b.is_relative_to(a)


def private_dir(path):
    canonical(path, missing=True)
    path.mkdir(mode=0o700, parents=True, exist_ok=True)
    s = path.stat()
    require(s.st_uid == os.getuid() and stat.S_IMODE(s.st_mode) == 0o700,
            'state and mount directories must be owned by this user and mode 0700')


def run(args):
    p = subprocess.run([str(x) for x in args], capture_output=True, text=True)
    require(p.returncode == 0, 'command failed: ' + str(args[0]) + ': ' + p.stderr[-1500:])
    return p.stdout


def image_info():
    return plistlib.loads(subprocess.check_output(['/usr/bin/hdiutil', 'info', '-plist']))['images']


def active_use(paths):
    """Failure to inspect processes is a hold, not an empty result."""
    ps = run(['ps', '-axo', 'pid=,command='])
    ls = run(['lsof', '-nP', '-Fpn'])
    for p in paths:
        aliases = {str(p)}
        if str(p).startswith('/private/'):
            aliases.add(str(p)[8:])
        for alias in aliases:
            require(alias not in ps and not any(
                line == 'n' + alias or line.startswith('n' + alias + '/')
                for line in ls.splitlines()), 'active process/open file: ' + str(p))


def metadata(path):
    require(sys.platform == 'darwin', 'macOS APFS adapter required; this host is not qualified')
    from archive_metadata import metadata as collect
    m = collect(path)
    m['xattrs'].pop('com.apple.provenance', None)
    m.pop('birthtime', None)
    if m['type'] == 'file':
        m['sha256'] = digest(path)
        s = path.lstat()
        require([s.st_dev, s.st_ino, s.st_ctime_ns, s.st_nlink] == m['identity']
                and s.st_size == m['size'] and s.st_mtime_ns == m['mtime_ns'],
                'source changed during hashing: ' + str(path))
    return m


def walk(root):
    require(not os.path.ismount(root), 'run root is a mountpoint')
    device = root.lstat().st_dev
    yield root
    for parent, dirs, files in os.walk(root, followlinks=False):
        dirs.sort()
        files.sort()
        for name in dirs + files:
            path = Path(parent) / name
            require(path.lstat().st_dev == device and (path.is_symlink() or not os.path.ismount(path)),
                    'nested mount/filesystem boundary: ' + str(path))
            yield path


def rows(path):
    with gzip.open(path, 'rt') as f:
        for line in f:
            yield json.loads(line)


def inventory(source, manifest, max_entries=100000):
    require(not manifest.exists(), 'inventory already exists')
    total = allocated = count = 0
    hardlinks = {}
    with gzip.open(manifest, 'xt', compresslevel=3) as out:
        os.chmod(manifest, 0o600)
        for p in walk(source):
            require(count < max_entries, 'run exceeds configured entry-count budget')
            rel = str(p.relative_to(source))
            require(not any(x in p.parts for x in ['.private', '.git']), 'protected/worktree path: ' + str(p))
            require('\n' not in str(p) and '\r' not in str(p), 'unsupported newline in path')
            m = metadata(p)
            if m['type'] == 'symlink':
                require(not Path(m['target']).is_absolute() and p.resolve().is_relative_to(source) and p.exists(),
                        'absolute, external or dangling symlink requires a hold: ' + str(p))
            if m['type'] == 'file':
                total += m['size']
                allocated += m['allocated']
                if m['identity'][3] > 1:
                    key = tuple(m['identity'][:2])
                    group = hardlinks.setdefault(key, [0, m['identity'][3]])
                    group[0] += 1
            out.write(json.dumps({'path': rel, **m}, separators=(',', ':')) + '\n')
            count += 1
    require(all(count == expected for count, expected in hardlinks.values()),
            'hardlink outside selected root requires a dependency hold')
    with manifest.open('rb') as f:
        os.fsync(f.fileno())
    return {'entries': count, 'logical_bytes': total, 'allocated_bytes': allocated,
            'manifest_sha256': digest(manifest)}


def verify(root, manifest, gid_map, *, original=False):
    paths = iter(walk(root))
    hardlinks = {}
    reverse_links = {}
    count = 0
    for row in rows(manifest):
        p = next(paths, None)
        require(p is not None and str(p.relative_to(root)) == row['path'], 'path set changed')
        got = metadata(p)
        for key in ['type', 'mode', 'uid', 'gid', 'mtime_ns', 'flags', 'acl', 'xattrs', 'size', 'target', 'sha256']:
            expected = row.get(key)
            if key == 'gid' and not original:
                expected = gid_map.get(str(expected), expected)
            require(got.get(key) == expected, 'content/metadata mismatch: ' + str(p) + ': ' + key)
        if original:
            require(got['identity'] == row['identity'], 'source identity changed: ' + str(p))
        if got['type'] == 'file':
            a, b = tuple(row['identity'][:2]), tuple(got['identity'][:2])
            require(hardlinks.setdefault(a, b) == b and reverse_links.setdefault(b, a) == a,
                    'hardlink topology changed')
        count += 1
    require(next(paths, None) is None, 'unexpected additional paths')
    return count


class Archiver:
    def __init__(self, config):
        self.config_path = canonical(config)
        s = self.config_path.stat()
        require(s.st_uid == os.getuid() and stat.S_IMODE(s.st_mode) == 0o600, 'configuration must be owned by this user and mode 0600')
        self.c = json.loads(self.config_path.read_text())
        require(self.c.get('schema') == 1 and self.c.get('mode') in ['plan', 'archive'], 'invalid policy schema/mode')
        self.state = canonical(self.c['state_dir'], missing=True)
        self.mounts = canonical(self.c['image_mounts'], missing=True)
        self.share = canonical(self.c['archive_mount'], missing=True)
        self.archive = self.share / self.c['archive_subdir']
        require(self.c['archive_subdir'] and not Path(self.c['archive_subdir']).is_absolute()
                and '..' not in Path(self.c['archive_subdir']).parts, 'invalid archive subdirectory')
        self.allowed = [canonical(p) for p in self.c['allowed_roots']]
        require(not any(overlap(a, b) for a, b in [(self.state, self.share),
                (self.mounts, self.share), (self.state, self.mounts)]),
                'state, image mount roots and archive share must be disjoint')
        holds = canonical(self.c['holds_file'])
        require(all(type(self.c.get(k)) is int and self.c[k] >= 0
                    for k in ['max_run_bytes', 'min_free_bytes']), 'nonnegative byte budgets required')
        self.gid_map = self.c.get('gid_map', {})
        self.max_entries = self.c.get('max_entries', 100000)
        require(type(self.max_entries) is int and self.max_entries > 0, 'positive entry-count budget required')
        require(all(k.isdigit() and type(v) is int for k, v in self.gid_map.items()), 'invalid group mapping')
        require(self.allowed and all(not overlap(p, q) for p in self.allowed
                for q in [self.state, self.mounts, self.share, self.config_path, holds]), 'storage/config overlaps source roots')
        self.policy_identity = hashlib.sha256(json.dumps({k: self.c.get(k) for k in [
            'state_dir', 'image_mounts', 'archive_mount', 'archive_export', 'archive_subdir',
            'archive_export_aliases', 'allowed_roots', 'holds_file', 'gid_map']}, sort_keys=True).encode()).hexdigest()

    @contextlib.contextmanager
    def locked(self):
        private_dir(self.state)
        # macOS mount flags distinguish local storage from NFS/SMB destinations.
        candidates = []
        for line in run(['/sbin/mount']).splitlines():
            if ' on ' not in line or ' (' not in line:
                continue
            mount_path, flags = line.split(' on ', 1)[1].rsplit(' (', 1)
            if self.state.is_relative_to(Path(mount_path)):
                candidates.append((len(Path(mount_path).parts), flags.rstrip(')').split(', ')))
        require(candidates and 'local' in max(candidates)[1], 'transaction state must be on a local filesystem')
        path = self.state / 'host.lock'
        fd = os.open(path, os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW, 0o600)
        try:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise Held('another storage operation owns the host lock')
            yield
        finally:
            os.close(fd)

    def check_mount(self):
        canonical(self.share)
        require(os.path.ismount(self.share), 'archive mount is unavailable')
        # statfs-derived mount table binds the exact export; DNS lookup is not used.
        exports = [self.c['archive_export']] + self.c.get('archive_export_aliases', [])
        require(all(isinstance(x, str) and ':/' in x and '\n' not in x for x in exports), 'invalid export identity')
        prefixes = [x + ' on ' + str(self.share) + ' (nfs,' for x in exports]
        require(any(x.startswith(prefix) for x in run(['/sbin/mount']).splitlines() for prefix in prefixes), 'wrong archive export')
        canonical(self.archive, missing=True)
        private_dir(self.archive)

    def key(self, project, iteration):
        require(all(isinstance(s, str) and re.fullmatch('[a-z0-9][a-z0-9-]{0,63}', s)
                    for s in [project, iteration]), 'invalid project/iteration ID')
        return project + '--' + iteration

    def location(self, key):
        require(re.fullmatch('[a-z0-9-]+--[a-z0-9-]+', key) is not None, 'invalid run key')
        return self.state / (key + '.json')

    def hold_check(self, record):
        path = canonical(self.c['holds_file'])
        require(path.stat().st_uid == os.getuid() and stat.S_IMODE(path.stat().st_mode) == 0o600,
                'host hold registry must be owned by this user and mode 0600')
        holds = json.loads(path.read_text())
        require(holds.get('schema') == 1 and isinstance(holds.get('holds'), list), 'invalid host hold registry')
        source = Path(record['source'])
        require(record['execution'] == 'closed' and record['released'] is True,
                'run is active or not released')
        require(not record['dependencies'], 'current/queued dependencies retain this run')
        for hold in holds['holds']:
            p = canonical(hold['path'], missing=True)
            require(not overlap(source, p), 'host dependency hold: ' + hold['reason'])

    def register(self, record):
        require(record.get('schema') == 1, 'invalid run schema')
        key = self.key(record['project'], record['iteration'])
        source = canonical(record['source'])
        require(source.is_dir() and source.name not in ['.git', '.private'], 'run root must be an ordinary directory')
        require(any(source != p and source.is_relative_to(p) for p in self.allowed), 'source outside registered scratch roots')
        require(record.get('execution') in ['active', 'closed'] and type(record.get('released')) is bool
                and isinstance(record.get('dependencies'), list), 'explicit execution, release and dependencies required')
        require(record.get('result') in ['pending', 'accepted', 'rejected', 'failed', 'invalid', 'inconclusive'], 'invalid scientific result')
        require(record.get('classification') in ['private', 'personal', 'internal', 'public'], 'classification required')
        require(record.get('evidence') and isinstance(record['evidence'], str), 'durable evidence reference required')
        target = self.location(key)
        if target.exists():
            old = json.loads(target.read_text())
            require(old['phase'] == 'registered' and old['record']['source'] == str(source), 'registered source changed or transaction already started')
        for other in self.state.glob('*--*.json'):
            if other == target:
                continue
            saved = json.loads(other.read_text())
            require(not overlap(source, Path(saved['record']['source'])), 'overlapping registered run')
        write_json(target, {'schema': 1, 'key': key, 'record': record, 'phase': 'registered',
                            'policy_identity': self.policy_identity})
        return {'run': key, 'phase': 'registered'}

    def save(self, tx, phase, **values):
        tx.update(values, phase=phase, updated_at=time.time())
        write_json(self.location(tx['key']), tx)
        self.fault(phase)

    def fault(self, phase):
        """No production fault switch. Tests override this method."""

    def paths(self, tx):
        key = tx['key']
        return (Path(tx['record']['source']), self.state / (key + '.dmg'),
                self.archive / (key + '.dmg'), self.mounts / key,
                self.state / (key + '.jsonl.gz'))

    def ensure_image(self, image, mount):
        private_dir(self.mounts)
        canonical(mount, missing=True)
        if not os.path.ismount(mount):
            private_dir(mount)
            require(not any(mount.iterdir()), 'mountpoint contains local files')
            for attempt in range(3):
                try:
                    run(['/usr/bin/hdiutil', 'attach', '-noverify', '-readonly', '-owners', 'on', '-nobrowse', '-mountpoint', mount, image])
                    break
                except Held as exc:
                    if os.path.ismount(mount):
                        break  # Exact backing/read-only verification still follows.
                    if 'Resource temporarily unavailable' not in str(exc) or attempt == 2:
                        raise
                    time.sleep(attempt + 1)
        require(any(Path(i.get('image-path', '/')) == image and i.get('writeable') is False
                    and any(e.get('mount-point') == str(mount) for e in i.get('system-entities', []))
                    for i in image_info()), 'wrong or writable image mount')

    def create_image(self, source, image, mount, manifest):
        # A second, empty object makes hdiutil preserve the source root itself.
        marker = self.state / 'container-marker'
        private_dir(marker)
        require(not any(marker.iterdir()) and source.name != marker.name, 'container marker collision')
        run(['/usr/bin/hdiutil', 'create', '-fs', 'APFS', '-format', 'ULFO', '-volname', image.stem,
             '-anyowners', '-nospotlight', '-srcfolder', source, '-srcfolder', marker, image])
        image.chmod(0o600)
        links = [r for r in rows(manifest) if r['type'] == 'symlink']
        if links:
            private_dir(self.mounts)
            private_dir(mount)
            shadow = image.with_suffix('.shadow')
            fixed = image.with_suffix('.fixed.dmg')
            require(not shadow.exists() and not fixed.exists(), 'unfinished metadata repair')
            run(['/usr/bin/hdiutil', 'attach', '-noverify', '-owners', 'on', '-nobrowse', '-shadow', shadow,
                 '-mountpoint', mount, image])
            for row in links:
                p = mount / source.name / row['path']
                require(p.is_symlink() and os.readlink(p) == row['target'], 'image symlink changed')
                os.utime(p, ns=(row['mtime_ns'], row['mtime_ns']), follow_symlinks=False)
            run(['/usr/bin/hdiutil', 'detach', mount])
            run(['/usr/bin/hdiutil', 'convert', '-format', 'ULFO', '-shadow', shadow, '-o', fixed, image])
            fixed.chmod(0o600)
            os.replace(fixed, image)
            shadow.unlink()

    def copy_verified(self, source, dest):
        require(source.resolve() != dest.resolve(strict=False), 'source and archive destination overlap')
        sha = digest(source)
        partial = dest.with_name(dest.name + '.partial')
        if os.path.lexists(dest):
            require(not dest.is_symlink() and dest.is_file() and digest(dest) == sha, 'archive destination collision')
            if os.path.lexists(partial):
                require(not partial.is_symlink() and partial.is_file() and digest(partial) == sha, 'unexpected partial beside completed archive')
                partial.unlink()
                sync_dir(dest.parent)
            return sha
        if os.path.lexists(partial):
            require(not partial.is_symlink() and partial.is_file(), 'partial path collision')
            before = partial.stat()
            require(before.st_size <= source.stat().st_size, 'oversized partial copy retained')
            with source.open('rb') as src, partial.open('r+b') as dst:
                require(os.fstat(dst.fileno()).st_ino == before.st_ino, 'partial identity changed')
                remaining = before.st_size
                while remaining:
                    size = min(4 * 1024 * 1024, remaining)
                    require(src.read(size) == dst.read(size), 'partial copy prefix mismatch; retained for review')
                    remaining -= size
                shutil.copyfileobj(src, dst, 4 * 1024 * 1024)
                dst.flush()
                os.fsync(dst.fileno())
        else:
            with source.open('rb') as src, partial.open('xb') as dst:
                os.chmod(partial, 0o600)
                shutil.copyfileobj(src, dst, 4 * 1024 * 1024)
                dst.flush()
                os.fsync(dst.fileno())
        require(digest(partial) == sha, 'archive checksum mismatch')
        self.fault('before-publish')
        # NFS LINK is atomic and fails when the destination exists; rename is not.
        os.link(partial, dest, follow_symlinks=False)
        sync_dir(dest.parent)
        partial.unlink()
        sync_dir(dest.parent)
        return sha

    def closeout(self, key, execute=False):
        tx = json.loads(self.location(key).read_text())
        require(tx['key'] == key, 'transaction identity mismatch')
        require(tx.get('policy_identity') == self.policy_identity, 'run belongs to a different storage policy; explicit migration required')
        source, image, remote, mount, manifest = self.paths(tx)
        if tx['phase'] != 'complete':
            self.hold_check(tx['record'])
        if not execute or self.c['mode'] != 'archive':
            return {'run': key, 'phase': tx['phase'], 'eligible': True, 'executed': False}
        self.check_mount()
        require(sys.platform == 'darwin', 'only macOS APFS adapter is qualified')
        if tx['phase'] == 'registered':
            active_use([source])
            canonical(source)
            self.save(tx, 'inventory-started')
            info = inventory(source, manifest, self.max_entries)
            require(info['logical_bytes'] <= self.c['max_run_bytes'], 'run exceeds configured batch budget')
            needed = int(max(info['logical_bytes'], info['allocated_bytes']) * 2.5) + 1024**3
            require(shutil.disk_usage(self.state).free > needed + self.c['min_free_bytes'], 'insufficient local staging headroom')
            require(shutil.disk_usage(self.archive).free > needed, 'insufficient archive capacity')
            self.save(tx, 'inventoried', **info)
        require(tx['phase'] != 'inventory-started', 'interrupted inventory retained; source unchanged, inspect and reset transaction')
        require(digest(manifest) == tx['manifest_sha256'], 'manifest changed')
        if tx['phase'] == 'inventoried':
            active_use([source])
            require(not image.exists(), 'unfinished image retained; inspect and reset transaction')
            self.create_image(source, image, mount, manifest)
            self.save(tx, 'image-created')
        if tx['phase'] == 'image-created':
            self.ensure_image(image, mount)
            verify(mount / source.name, manifest, self.gid_map)
            run(['/usr/bin/hdiutil', 'detach', mount])
            self.save(tx, 'image-verified', image_sha256=digest(image))
        if tx['phase'] == 'image-verified':
            require(digest(image) == tx['image_sha256'], 'verified staging image changed')
            self.copy_verified(image, remote)
            self.copy_verified(manifest, self.archive / manifest.name)
            st = remote.stat()
            self.save(tx, 'remote-verified', remote_identity=[st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns])

        recovery_dir = self.state / 'recovery'
        private_dir(recovery_dir)
        recovery_file = recovery_dir / (key + '.json')
        recovery = {'schema': 1, 'format': 'macos-apfs-ulfo', 'record': tx['record'],
                    'image': str(remote), 'image_sha256': tx['image_sha256'],
                    'manifest': manifest.name, 'manifest_sha256': tx['manifest_sha256'],
                    'original': str(source), 'mounted_target': str(mount / source.name),
                    'gid_map': self.gid_map, 'policy_identity': tx['policy_identity']}
        if recovery_file.exists():
            require(json.loads(recovery_file.read_text()) == recovery, 'recovery receipt changed')
        else:
            write_json(recovery_file, recovery)
        recovery_remote = self.archive / (key + '.recovery.json')
        self.copy_verified(recovery_file, recovery_remote)
        companions = [self.archive / manifest.name, recovery_remote]
        for companion, expected in zip(companions, [tx['manifest_sha256'], digest(recovery_file)]):
            require(not companion.is_symlink() and digest(companion) == expected, 'recovery companion changed')
        companion_ids = [[p.stat().st_dev, p.stat().st_ino, p.stat().st_size, p.stat().st_mtime_ns] for p in companions]

        def remote_guard():
            self.check_mount()
            require(not remote.is_symlink() and remote.is_file(), 'NAS image missing or replaced')
            st = remote.stat()
            require([st.st_dev, st.st_ino, st.st_size, st.st_mtime_ns] == tx['remote_identity'], 'NAS image identity changed')
            for p, expected in zip(companions, companion_ids):
                require(not p.is_symlink() and p.is_file(), 'recovery companion unavailable')
                s = p.stat()
                require([s.st_dev, s.st_ino, s.st_size, s.st_mtime_ns] == expected, 'recovery companion identity changed')

        remote_guard()
        if tx['phase'] != 'complete' or not os.path.ismount(mount):
            require(digest(remote) == tx['image_sha256'], 'NAS image changed')
        self.ensure_image(remote, mount)
        target = mount / source.name
        if tx['phase'] == 'remote-verified':
            verify(source, manifest, {}, original=True)
            self.hold_check(tx['record'])
            active_use([source])
            self.save(tx, 'ready', target=str(target))
        holding = source.with_name('.iteration-archive-retiring-' + key)
        if tx['phase'] == 'ready':
            self.hold_check(tx['record'])
            active_use([source, holding])
            remote_guard()
            if not holding.exists():
                verify(source, manifest, {}, original=True)
                remote_guard()
                require(not source.is_symlink(), 'unexpected source link')
                os.rename(source, holding)
                sync_dir(source.parent)
                self.fault('after-rename')
            require(holding.is_dir() and not holding.is_symlink(), 'retirement holding path changed')
            original_root = next(rows(manifest))
            held_stat = holding.lstat()
            require([held_stat.st_dev, held_stat.st_ino] == original_root['identity'][:2], 'holding root identity changed')
            if not os.path.lexists(source):
                source.symlink_to(target)
                sync_dir(source.parent)
                self.fault('after-link')
            require(source.is_symlink() and source.resolve() == target and target.exists(), 'original path collision')
            self.save(tx, 'linked')
        if tx['phase'] == 'linked':
            require(source.is_symlink() and source.resolve() == target and target.exists(), 'archive link changed')
            self.hold_check(tx['record'])
            active_use([holding])
            remote_guard()
            self.retire(holding, manifest)
            remote_guard()
            self.save(tx, 'retired')
        if tx['phase'] == 'retired':
            remote_guard()
            if image.exists():
                require(digest(image) == tx['image_sha256'], 'staging collision')
                remote_guard()
                image.unlink()
            self.save(tx, 'complete', free_bytes=shutil.disk_usage(self.state).free)
        require(tx['phase'] == 'complete', 'unknown transaction phase')
        if not os.path.lexists(source):
            canonical(source.parent)
            require(any(source != p and source.is_relative_to(p) for p in self.allowed), 'original outside registered scratch roots')
            remote_guard()
            source.symlink_to(target)
            sync_dir(source.parent)
        require(source.is_symlink() and source.resolve() == target and target.exists(), 'completed original link unavailable')
        self.copy_verified(self.location(key), self.archive / (key + '.receipt.json'))
        return {'run': key, 'phase': 'complete', 'source': str(source), 'target': str(target),
                'entries': tx['entries'], 'image_sha256': tx['image_sha256']}

    def retire(self, holding, manifest):
        """Resume exact-entry retirement; unknown or modified entries stop it."""
        expected = list(rows(manifest))
        if not holding.exists():
            return
        known = {r['path'] for r in expected}
        require(all(str(p.relative_to(holding)) in known for p in walk(holding)), 'unexpected file in retirement holding directory')
        for row in reversed(expected):
            p = holding / row['path']
            if not os.path.lexists(p):
                continue
            got = metadata(p)
            require(got['identity'][:2] == row['identity'][:2], 'retirement identity changed')
            for k in ['type', 'mode', 'uid', 'gid', 'flags', 'acl', 'xattrs', 'size', 'target', 'sha256']:
                require(got.get(k) == row.get(k), 'retirement metadata/content changed: ' + str(p))
            if got['type'] != 'directory':
                require(got['mtime_ns'] == row['mtime_ns'], 'retirement file changed')
                p.unlink()
            else:
                p.rmdir()
            self.fault('retire-entry')
        sync_dir(holding.parent)

    def restore(self, key, destination):
        tx = json.loads(self.location(key).read_text())
        require(tx.get('policy_identity') == self.policy_identity, 'run belongs to a different storage policy; explicit migration required')
        require(tx['phase'] == 'complete', 'only completed archives can be restored')
        source, image, remote, mount, manifest = self.paths(tx)
        destination = canonical(destination, missing=True)
        require(not os.path.lexists(destination), 'restore destination already exists')
        require(not any(overlap(destination, p) for p in [self.state, self.mounts, self.share, source]), 'restore overlaps storage/source')
        self.check_mount()
        require(digest(remote) == tx['image_sha256'] and digest(manifest) == tx['manifest_sha256'], 'archive or manifest changed')
        self.ensure_image(remote, mount)
        require(shutil.disk_usage(destination.parent).free > tx['logical_bytes'] + self.c['min_free_bytes'], 'insufficient restoration space')
        run(['/usr/bin/ditto', '--rsrc', '--extattr', '--acl', mount / source.name, destination])
        for row in rows(manifest):
            if row['type'] == 'symlink':
                p = destination / row['path']
                os.utime(p, ns=(row['mtime_ns'], row['mtime_ns']), follow_symlinks=False)
        verify(destination, manifest, self.gid_map)
        return {'restored': str(destination), 'verified': True, 'group_mapping': self.gid_map}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--config', required=True)
    sub = p.add_subparsers(dest='command', required=True)
    register = sub.add_parser('register')
    register.add_argument('record')
    for name in ['plan', 'closeout']:
        command = sub.add_parser(name)
        command.add_argument('run')
        if name == 'closeout':
            command.add_argument('--execute', action='store_true')
    sub.add_parser('status')
    preflight = sub.add_parser('preflight')
    preflight.add_argument('--required-bytes', type=int, required=True)
    preflight.add_argument('--scratch-root')
    resume = sub.add_parser('resume')
    resume.add_argument('--execute', action='store_true')
    restore = sub.add_parser('restore')
    restore.add_argument('run')
    restore.add_argument('destination')
    args = p.parse_args()
    try:
        a = Archiver(args.config)
        with a.locked():
            if args.command == 'register':
                result = a.register(json.loads(Path(args.record).read_text()))
            elif args.command == 'preflight':
                require(args.required_bytes >= 0, 'required bytes must be nonnegative')
                if args.scratch_root:
                    scratch = canonical(args.scratch_root)
                    require(any(scratch.is_relative_to(root) for root in a.allowed), 'unregistered scratch filesystem')
                else:
                    require(len({root.stat().st_dev for root in a.allowed}) == 1, 'multiple scratch filesystems: supply --scratch-root')
                    scratch = a.allowed[0]
                free = shutil.disk_usage(scratch).free
                require(free >= args.required_bytes + a.c['min_free_bytes'], 'insufficient headroom for the next run')
                result = {'admitted': True, 'scratch_root': str(scratch), 'free_bytes': free, 'required_bytes': args.required_bytes,
                          'reserve_bytes': a.c['min_free_bytes']}
            elif args.command in ['plan', 'closeout']:
                result = a.closeout(args.run, getattr(args, 'execute', False))
            elif args.command == 'restore':
                result = a.restore(args.run, args.destination)
            else:
                result = []
                for path in sorted(a.state.glob('*--*.json')):
                    tx = json.loads(path.read_text())
                    try:
                        result.append(a.closeout(tx['key'], getattr(args, 'execute', False)))
                    except (Held, OSError, ValueError, KeyError) as exc:
                        result.append({'run': tx['key'], 'phase': tx['phase'], 'held': str(exc)})
                result = {'runs': result, 'free_bytes': shutil.disk_usage(a.state).free}
        print(json.dumps(result, indent=2))
    except (Held, OSError, ValueError, KeyError, subprocess.SubprocessError) as exc:
        print(json.dumps({'held': str(exc), 'originals_retained_unless_verified_cutover_already_recorded': True}))
        return 2
    return 0


if __name__ == '__main__':
    sys.exit(main())
