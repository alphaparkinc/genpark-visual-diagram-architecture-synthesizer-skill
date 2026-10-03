"""Example usage for VisualDiagramArchitectureSynthesizer."""
import sys
import json
from client import VisualDiagramArchitectureSynthesizer

sys.stdout.reconfigure(encoding='utf-8')

def main():
    print("=== Visual Diagram-to-Code Architecture Synthesizer Demo ===")
    synthesizer = VisualDiagramArchitectureSynthesizer()

    nodes = [
        {"id": "client_app", "label": "Client App (Ray-Ban / Muse)", "type": "process"},
        {"id": "agent_hub", "label": "GenPark Autonomous Agent Hub", "type": "process"},
        {"id": "vector_vault", "label": "Memory Vector Vault", "type": "database"},
        {"id": "merchant_api", "label": "Shopify / Expedia Connector", "type": "service"}
    ]
    edges = [
        {"source_id": "client_app", "target_id": "agent_hub", "relation": "User Voice Intent"},
        {"source_id": "agent_hub", "target_id": "vector_vault", "relation": "Episodic Context"},
        {"source_id": "agent_hub", "target_id": "merchant_api", "relation": "Execute Booking"}
    ]

    print("\n--- Synthesizing Architecture from Diagram ---")
    res = synthesizer.synthesize_architecture_from_diagram("Consumer Agent Topology", nodes, edges)
    print("Generated Mermaid Diagram:")
    print(res["mermaid_markdown"])

    print("\nGenerated Code Scaffolding:")
    print(res["code_scaffold"])

if __name__ == "__main__":
    main()
