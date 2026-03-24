"""UT-009: MCP server — tool registration."""


class TestMcpToolRegistration:
    async def test_three_tools_registered(self):
        """The MCP server must expose exactly 3 tools."""
        from server.MCPServer import mcp
        tools = await mcp.list_tools()
        assert len(tools) == 3

    async def test_tool_names(self):
        """All three expected tool names are registered."""
        from server.MCPServer import mcp
        tools = await mcp.list_tools()
        names = {t.name for t in tools}
        assert names == {"search_knowledge_base", "get_ospf", "get_interfaces"}
