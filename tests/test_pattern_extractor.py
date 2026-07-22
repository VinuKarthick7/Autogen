import pytest
import os
from knowledge.pattern_extractor import PatternExtractor

def test_pattern_extractor(tmp_path):
    patterns_dir = os.path.join(tmp_path, "patterns")
    extractor = PatternExtractor(patterns_dir)
    
    code_data = {"file1": "This uses a Coupon in the logic."}
    patterns = extractor.extract_patterns("pms", code_data)
    
    assert len(patterns) == 1
    assert patterns[0]["pattern"] == "Coupon pattern"
    assert patterns[0]["repo"] == "pms"
    
    extractor.save_patterns("coupon", patterns)
    assert os.path.exists(os.path.join(patterns_dir, "coupon_patterns.json"))
