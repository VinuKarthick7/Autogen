import argparse
from knowledge.global_symbol_index import GlobalSymbolIndex

def search():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    args = parser.parse_args()
    
    idx = GlobalSymbolIndex()
    # Let's add a fake symbol if empty for demonstration
    if not idx.index:
        idx.index_repository("pms", [{"symbol": "CouponService", "file": "app/services/coupon.py"}])
        
    results = idx.search(args.query)
    for r in results:
        print(f"[{r.get('repository')}] {r.get('symbol')} in {r.get('file')}")
        
if __name__ == "__main__":
    search()
