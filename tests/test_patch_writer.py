import os
import shutil
import pytest
from executor.patch_writer import PatchWriter
from schemas.generated_file import GeneratedFile

def test_patch_writer():
    repo_path = "test_patch_repo"
    os.makedirs(repo_path, exist_ok=True)
    
    try:
        writer = PatchWriter(repo_path)
        
        # Test create
        f1 = GeneratedFile(path="new.txt", content="hello", file_type="txt")
        op1 = writer.generate_operation(f1)
        assert op1.operation == "create"
        
        writer.apply_operation(op1)
        assert os.path.exists(os.path.join(repo_path, "new.txt"))
        
        # Test modify
        f2 = GeneratedFile(path="new.txt", content="hello world", file_type="txt")
        op2 = writer.generate_operation(f2)
        assert op2.operation == "modify"
        assert op2.old_content == "hello"
        
        writer.apply_operation(op2)
        with open(os.path.join(repo_path, "new.txt"), "r") as f:
            assert f.read() == "hello world"
            
        # Test restricted
        f_restricted = GeneratedFile(path=".env", content="secret=1", file_type="txt")
        with pytest.raises(ValueError, match="Access to restricted path denied"):
            writer.generate_operation(f_restricted)
            
    finally:
        shutil.rmtree(repo_path, ignore_errors=True)
