"""macOS metadata collection; provenance and birthtime are not restoration guarantees."""
import os,stat,hashlib,base64,ctypes
lib=ctypes.CDLL('/usr/lib/libSystem.B.dylib',use_errno=True)
lib.acl_get_link_np.argtypes=[ctypes.c_char_p,ctypes.c_int];lib.acl_get_link_np.restype=ctypes.c_void_p
lib.acl_to_text.argtypes=[ctypes.c_void_p,ctypes.POINTER(ctypes.c_ssize_t)];lib.acl_to_text.restype=ctypes.c_void_p
lib.acl_free.argtypes=[ctypes.c_void_p]
lib.listxattr.argtypes=[ctypes.c_char_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_int];lib.listxattr.restype=ctypes.c_ssize_t
lib.getxattr.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_void_p,ctypes.c_size_t,ctypes.c_uint32,ctypes.c_int];lib.getxattr.restype=ctypes.c_ssize_t
def check(ok, p):
 if not ok:raise OSError(ctypes.get_errno(),str(p))
def xattrs(p):
 raw=os.fsencode(p);n=lib.listxattr(raw,None,0,1);check(n>=0,p)
 b=ctypes.create_string_buffer(n);check(lib.listxattr(raw,b,n,1)==n,p)
 result={}
 for name in b.raw.split(b'\0'):
  if not name:continue
  n=lib.getxattr(raw,name,None,0,0,1);check(n>=0,p)
  v=ctypes.create_string_buffer(n);check(lib.getxattr(raw,name,v,n,0,1)==n,p)
  result[name.decode()]=base64.b64encode(v.raw).decode()
 return result
def acl(p):
 a=lib.acl_get_link_np(os.fsencode(p),0x100)
 if not a:
  e=ctypes.get_errno()
  if e in (2,22,45,93):return None
  raise OSError(e,str(p))
 n=ctypes.c_ssize_t();b=lib.acl_to_text(a,ctypes.byref(n))
 try:
  if not b:raise OSError(ctypes.get_errno(),str(p))
  return ctypes.string_at(b,n.value).decode()
 finally:
  if b:lib.acl_free(b)
  lib.acl_free(a)
def digest(p):
 h=hashlib.sha256()
 with open(p,'rb') as f:
  for b in iter(lambda:f.read(4*1024*1024),b''):h.update(b)
 return h.hexdigest()
def metadata(p):
 s=p.lstat()
 kind='file' if stat.S_ISREG(s.st_mode) else 'directory' if stat.S_ISDIR(s.st_mode) else 'symlink' if stat.S_ISLNK(s.st_mode) else 'unsupported'
 if kind=='unsupported':raise ValueError('unsupported filesystem object: '+str(p))
 return dict(type=kind,mode=stat.S_IMODE(s.st_mode),uid=s.st_uid,gid=s.st_gid,mtime_ns=s.st_mtime_ns,flags=s.st_flags,acl=acl(p),xattrs=xattrs(p),size=s.st_size if kind=='file' else None,target=os.readlink(p) if kind=='symlink' else None,identity=[s.st_dev,s.st_ino,s.st_ctime_ns,s.st_nlink],allocated=s.st_blocks*512,birthtime=s.st_birthtime)
