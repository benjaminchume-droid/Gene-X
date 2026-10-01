"""Small CLI adapter over the same Gene protocol used by other interfaces."""
from __future__ import annotations
import argparse
from .protocol import GeneRequest,ProtocolHandler

def build_parser()->argparse.ArgumentParser:
    parser=argparse.ArgumentParser(prog="gene")
    parser.add_argument("operation")
    parser.add_argument("payload",nargs="*",default=[])
    return parser

def main(handler:ProtocolHandler|None=None,argv=None)->int:
    parser=build_parser();args=parser.parse_args(argv)
    response=(handler or ProtocolHandler()).handle(GeneRequest(args.operation,{"args":args.payload}))
    if response.success:
        print(response.payload);return 0
    print(response.error);return 1
