"""UT-009: MCP server — tool registration."""


class TestMcpToolRegistration:
    async def test_eight_tools_registered(self):
        """The MCP server must expose exactly 8 tools."""
        from server.MCPServer import mcp
        tools = await mcp.list_tools()
        assert len(tools) == 8

    async def test_tool_names(self):
        """All eight expected tool names are registered."""
        from server.MCPServer import mcp
        tools = await mcp.list_tools()
        names = {t.name for t in tools}
        assert names == {
            "search_knowledge_base",
            "get_ospf",
            "get_interfaces",
            "get_routing",
            "query_intent",
            "get_status",
            "list_devices",
            "traceroute",
        }
