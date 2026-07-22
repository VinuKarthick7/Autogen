import pytest
import os
from knowledge.cross_repo_graph import CrossRepoGraph

def test_graph(tmp_path):
    graph_file = os.path.join(tmp_path, "graph.json")
    graph = CrossRepoGraph(graph_file)
    graph.add_node("r1", "repository")
    graph.add_node("r2", "repository")
    graph.add_edge("r1", "r2", "similarity", weight=0.9)
    
    graph.build_graph()
    
    matches = graph.find_similar_repositories("r1")
    assert len(matches) == 1
    assert matches[0].target_repo == "r2"
    assert matches[0].similarity_score == 0.9
