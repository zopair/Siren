from siren_trap.siren_lure.mcp_server import SirenMCPServer


def test_mcp_initialize_negotiates_protocol_version():
    response = SirenMCPServer().handle(
        {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {"protocolVersion": "2025-03-26"},
        }
    )

    assert response["result"]["protocolVersion"] == "2025-03-26"
    assert "tools" in response["result"]["capabilities"]


def test_mcp_rejects_unknown_tool_without_side_effects():
    response = SirenMCPServer().handle(
        {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/call",
            "params": {"name": "execute_shell", "arguments": {}},
        }
    )

    assert response["error"]["code"] == -32602
