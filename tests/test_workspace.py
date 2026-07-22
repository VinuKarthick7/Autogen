import os
import shutil
import pytest
from executor.workspace import WorkspaceManager

def test_workspace_manager():
    mgr = WorkspaceManager("test_workspaces")
    
    # Create a dummy source repo
    os.makedirs("dummy_repo", exist_ok=True)
    with open("dummy_repo/test.txt", "w") as f:
        f.write("hello")
        
    run_id = "test_run"
    target_dir = os.path.join(mgr.create_workspace(run_id), "repo")
    mgr.copy_repository("dummy_repo", target_dir)
    
    assert os.path.exists(os.path.join(target_dir, "test.txt"))
    
    mgr.cleanup_workspace(run_id)
    assert not os.path.exists(target_dir)
    
    # Clean up dummy repo
    shutil.rmtree("dummy_repo")
