"""MCP Server for Visual Diagram Architecture Synthesizer."""
import sys
import json
import time
from client import VisualDiagramArchitectureSynthesizer

synthesizer = VisualDiagramArchitectureSynthesizer()

def handle_call_tool(params):
    name = params.get("name")
    args = params.get("arguments", {})
    if name != "synthesize_architecture_diagram":
        raise ValueError(f"Unknown tool: {name}")

    action = args.get("action", "synthesize_architecture_from_diagram")
    if action == "synthesize_architecture_from_diagram":
        return synthesizer.synthesize_architecture_from_diagram(
            diagram_title=args.get("diagram_title", "System Architecture"),
            nodes=args.get("nodes", []),
            edges=args.get("edges", [])
        )
    elif action == "generate_mermaid_graph":
        m = synthesizer.generate_mermaid_graph(
            diagram_title=args.get("diagram_title", "Diagram"),
            nodes=args.get("nodes", []),
            edges=args.get("edges", [])
        )
        return {"mermaid_markdown": m}
    elif action == "scaffold_python_classes":
        s = synthesizer.scaffold_python_classes(
            nodes=args.get("nodes", []),
            edges=args.get("edges", [])
        )
        return {"code_scaffold": s}
    else:
        raise ValueError(f"Invalid action: {action}")

def main():
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        print("Running self-test...")
        nodes = [
            {"id": "api_gw", "label": "API Gateway", "type": "process"},
            {"id": "auth_svc", "label": "Auth Service", "type": "process"},
            {"id": "user_db", "label": "User DB", "type": "database"}
        ]
        edges = [
            {"source_id": "api_gw", "target_id": "auth_svc", "relation": "verify_token"},
            {"source_id": "auth_svc", "target_id": "user_db", "relation": "lookup"}
        ]
        res = synthesizer.synthesize_architecture_from_diagram("Microservices", nodes, edges)
        assert "flowchart" in res["mermaid_markdown"]
        assert "class ApiGw" in res["code_scaffold"]
        print("Self-test PASSED!")
        sys.exit(0)

    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            req = json.loads(line)
            msg_id = req.get("id")
            method = req.get("method")
            if method == "initialize":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "serverInfo": {"name": "VisualDiagramArchitectureSynthesizer", "version": "1.0.0"},
                        "capabilities": {"tools": {}}
                    }
                }
            elif method == "tools/list":
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {
                        "tools": [{
                            "name": "synthesize_architecture_diagram",
                            "description": "Visual diagram to code: parse diagram node bounding boxes and connections, generate Mermaid diagram syntax, and synthesize modular skeleton code scaffolds.",
                            "inputSchema": {
                                "type": "object",
                                "properties": {
                                    "action": {"type": "string", "enum": ["synthesize_architecture_from_diagram", "generate_mermaid_graph", "scaffold_python_classes"]},
                                    "diagram_title": {"type": "string"},
                                    "nodes": {"type": "array"},
                                    "edges": {"type": "array"}
                                },
                                "required": ["action"]
                            }
                        }]
                    }
                }
            elif method == "tools/call":
                res = handle_call_tool(req.get("params", {}))
                resp = {
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "result": {"content": [{"type": "text", "text": json.dumps(res, indent=2)}]}
                }
            else:
                resp = {"jsonrpc": "2.0", "id": msg_id, "result": {}}
            print(json.dumps(resp), flush=True)
        except Exception as e:
            err_resp = {"jsonrpc": "2.0", "id": None, "error": {"code": -32000, "message": str(e)}}
            print(json.dumps(err_resp), flush=True)

if __name__ == "__main__":
    main()
