#!/usr/bin/env python3
import json,os,sys
from pathlib import Path
root=Path(__file__).resolve().parents[1]
config=Path(os.environ.get('ITERATION_ARCHIVE_CONFIG',str(root/'.local/iteration-archive.json')))
if not config.is_file():
 print(json.dumps({'storage':'unconfigured','action':'Configure the private policy before archival; preserve run evidence.'}))
 raise SystemExit(2)
os.execv(sys.executable,[sys.executable,str(root/'tools/iteration_archive/iteration_archive.py'),'--config',str(config),*sys.argv[1:]])
