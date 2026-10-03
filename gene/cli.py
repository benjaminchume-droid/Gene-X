from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from gene.system import GeneSystem

def build_parser():
 p=argparse.ArgumentParser(prog='gene'); s=p.add_subparsers(dest='command'); s.add_parser('health'); s.add_parser('init'); t=s.add_parser('think'); t.add_argument('input'); t.add_argument('--complexity',type=float,default=1.0); return p
def main(argv=None):
 a=build_parser().parse_args(argv)
 if a.command=='init':
  root=Path.home()/'.gene'; [ (root/n).mkdir(parents=True,exist_ok=True) for n in ('data','models','runs','config') ]; print(root); return 0
 g=GeneSystem()
 if a.command=='health': print(json.dumps(g.health(),indent=2,default=str)); return 0
 if a.command=='think':
  try: v=json.loads(a.input)
  except json.JSONDecodeError: v=a.input
  r=g.think(v,complexity=a.complexity); print(json.dumps({'mode':r.mode,'elapsed_seconds':r.elapsed_seconds,'value':r.value},default=str)); return 0
 build_parser().print_help(); return 0
if __name__=='__main__': sys.exit(main())
