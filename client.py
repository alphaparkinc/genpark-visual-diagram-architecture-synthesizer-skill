"""
Visual Diagram-to-Code Architecture Synthesizer (Zero External Dependencies)
Translates geometric diagram nodes and arrows into Mermaid diagrams and object skeletons.
"""
import time
import math
import hashlib
import json
from typing import Dict, Any, List, Optional

class VisualDiagramArchitectureSynthesizer:
    def __init__(self):
        pass

    def generate_mermaid_graph(
        self,
        diagram_title: str,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]],
        direction: str = "TD"
    ) -> str:
        """Compiles diagram nodes and edges into a clean GitHub-renderable Mermaid flowchart."""
        lines = [f"flowchart {direction}"]
        lines.append(f"    %% Diagram: {diagram_title}")

        # Render nodes
        for n in nodes:
            nid = n.get("id", "n")
            label = n.get("label", nid)
            ntype = n.get("type", "process")

            if ntype in ("database", "storage"):
                lines.append(f'    {nid}[("{label}")]')
            elif ntype in ("decision", "gateway"):
                lines.append(f'    {nid}{{"{label}"}}')
            elif ntype in ("queue", "event"):
                lines.append(f'    {nid}>"{label}"]')
            else: # process or service
                lines.append(f'    {nid}["{label}"]')

        # Render edges
        for e in edges:
            src = e.get("source_id")
            tgt = e.get("target_id")
            rel = e.get("relation", "")
            if rel:
                lines.append(f'    {src} -->|"{rel}"| {tgt}')
            else:
                lines.append(f'    {src} --> {tgt}')

        return "\n".join(lines)

    def scaffold_python_classes(
        self,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]]
    ) -> str:
        """Generates modular skeleton Python class definitions based on diagram components."""
        # Map incoming/outgoing
        outgoing = {}
        for e in edges:
            outgoing.setdefault(e.get("source_id"), []).append(e.get("target_id"))

        lines = [
            '"""Auto-generated architectural scaffolding from diagram."""',
            'from typing import Any, Dict, List, Optional',
            ''
        ]

        for n in nodes:
            nid = n.get("id", "Component")
            cls_name = "".join(part.capitalize() for part in nid.split("_"))
            label = n.get("label", cls_name)
            ntype = n.get("type", "Service")
            targets = outgoing.get(nid, [])

            lines.append(f'class {cls_name}:')
            lines.append(f'    """{label} ({ntype.upper()}) component."""')
            lines.append(f'    def __init__(self):')
            lines.append(f'        self.name = "{label}"')
            lines.append(f'        self.component_type = "{ntype}"')
            lines.append(f'        self.targets = {targets}')
            lines.append(f'')
            lines.append(f'    def process(self, payload: Dict[str, Any]) -> Dict[str, Any]:')
            lines.append(f'        # Execute logic for {label}')
            lines.append(f'        return {{"status": "OK", "source": "{nid}", "data": payload}}')
            lines.append(f'')

        return "\n".join(lines)

    def synthesize_architecture_from_diagram(
        self,
        diagram_title: str,
        nodes: List[Dict[str, Any]],
        edges: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Synthesizes complete package: Mermaid diagram, topology matrix, and Python code skeleton."""
        mermaid = self.generate_mermaid_graph(diagram_title, nodes, edges)
        scaffold = self.scaffold_python_classes(nodes, edges)

        return {
            "diagram_title": diagram_title,
            "total_nodes": len(nodes),
            "total_edges": len(edges),
            "mermaid_markdown": mermaid,
            "code_scaffold": scaffold,
            "topology_digest": hashlib.sha256(mermaid.encode("utf-8")).hexdigest()[:16]
        }
