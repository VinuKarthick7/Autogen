import os
import sys
from datetime import datetime
from knowledge.repository_registry import RepositoryRegistry
from schemas.repository_metadata import RepositoryMetadata

def index_mocks():
    registry = RepositoryRegistry()
    
    pms = RepositoryMetadata(
        repo_id="pms",
        name="PMS",
        path="/var/repos/pms",
        language="python",
        framework="fastapi",
        database="postgres",
        architecture_style="clean-architecture",
        modules=["auth", "rooms", "bookings", "coupons"],
        conventions={},
        indexed_at=datetime.utcnow()
    )
    
    erp = RepositoryMetadata(
        repo_id="erp",
        name="ERP",
        path="/var/repos/erp",
        language="python",
        framework="django",
        database="postgres",
        architecture_style="modular-monolith",
        modules=["auth", "finance", "inventory", "rewards", "audit"],
        conventions={},
        indexed_at=datetime.utcnow()
    )
    
    ecommerce = RepositoryMetadata(
        repo_id="ecommerce",
        name="E-Commerce",
        path="/var/repos/ecommerce",
        language="typescript",
        framework="express",
        database="mongo",
        architecture_style="microservices",
        modules=["users", "products", "cart", "discount"],
        conventions={},
        indexed_at=datetime.utcnow()
    )
    
    registry.register_repository(pms)
    registry.register_repository(erp)
    registry.register_repository(ecommerce)
    print("Mock repositories indexed successfully.")

if __name__ == "__main__":
    index_mocks()
