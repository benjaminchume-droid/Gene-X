"""MCP adapter: protocol transport into the unified capability layer."""
from dataclasses import dataclass
from typing import Any,Callable
from .capability import Capability
@dataclass(frozen=True)
class MCPToolDescription:
 name:str; description:str=""; input_schema:dict[str,Any]|None=None
class MCPAdapter:
 def __init__(self,invoke:Callable[[str,dict[str,Any]],Any],source="mcp"):self._invoke=invoke;self.source=source
 def capability(self,d):return Capability(d.name,d.description,lambda a:self._invoke(d.name,a),d.input_schema or {},source=self.source)
