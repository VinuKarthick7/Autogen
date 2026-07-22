import os
import shutil
from executor.git_manager import GitManager

def test_git_manager():
    repo_path = "test_git_repo"
    os.makedirs(repo_path, exist_ok=True)
    
    try:
        mgr = GitManager(repo_path)
        mgr.initialize()
        
        branch = mgr.create_branch("123")
        assert branch == "agent/run_123"
        
        with open(os.path.join(repo_path, "test.txt"), "w") as f:
            f.write("hello")
            
        diff = mgr.get_diff()
        assert "test.txt" in diff
        
        mgr.commit("Add test.txt")
        
        with open(os.path.join(repo_path, "test2.txt"), "w") as f:
            f.write("hello 2")
            
        mgr.rollback()
        assert not os.path.exists(os.path.join(repo_path, "test2.txt"))
        assert os.path.exists(os.path.join(repo_path, "test.txt"))
        
    finally:
        # Clean up
        shutil.rmtree(repo_path, ignore_errors=True)
