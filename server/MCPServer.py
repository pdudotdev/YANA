"""netKB MCP Server — OSPF knowledge base + live device tools."""
import logging
import sys
from pathlib import Path

# Ensure project root is on sys.path for module imports
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT))

from dotenv import load_dotenv
load_dotenv(_PROJECT_ROOT / ".env")

logging.basicConfig(level=logging.INFO, format="%(name)s: %(message)s")

from fastmcp import FastMCP
from tools.ospf import get_ospf
from tools.operational import get_interfaces
from tools.rag import search_knowledge_base

mcp = FastMCP("netkb")

mcp.tool(name="search_knowledge_base")(search_knowledge_base)
mcp.tool(name="get_ospf")(get_ospf)
mcp.tool(name="get_interfaces")(get_interfaces)

if __name__ == "__main__":
    mcp.run()
