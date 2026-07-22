from knowledge.cross_repo_graph import CrossRepoGraph

def build():
    graph = CrossRepoGraph()
    # Mocking graph edges based on mock repos
    graph.add_node("pms", "repository")
    graph.add_node("erp", "repository")
    graph.add_node("ecommerce", "repository")
    
    graph.add_edge("pms", "ecommerce", "similarity", weight=0.8)
    graph.add_edge("pms", "erp", "similarity", weight=0.6)
    
    graph.build_graph()
    print("Global graph built and saved.")
    
if __name__ == "__main__":
    build()
