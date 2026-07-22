import libcst as cst

class ModelVisitor(cst.CSTVisitor):
    def __init__(self, module: cst.Module):
        super().__init__()
        self.module = module
        self.models = []

    def visit_ClassDef(self, node: cst.ClassDef):
        is_base = False
        base_name = None
        for base in node.bases:
            if isinstance(base.value, cst.Name):
                if base.value.value == "Base":
                    is_base = True
                    base_name = "Base"
                    break
        
        if is_base:
            fields = []
            for statement in node.body.body:
                if isinstance(statement, cst.SimpleStatementLine):
                    for stmt in statement.body:
                        if isinstance(stmt, cst.AnnAssign):
                            if isinstance(stmt.target, cst.Name):
                                field_name = stmt.target.value
                                annotation_node = stmt.annotation.annotation
                                annotation_str = self.module.code_for_node(annotation_node)
                                # Storing as string format requested: "id: Mapped[UUID]"
                                fields.append(f"{field_name}: {annotation_str}")
            
            self.models.append({
                "name": node.name.value,
                "base": base_name,
                "fields": fields
            })

def extract_models(file_path: str) -> list[dict]:
    with open(file_path, "r", encoding="utf-8") as f:
        source_code = f.read()
    
    module = cst.parse_module(source_code)
    visitor = ModelVisitor(module)
    module.visit(visitor)
    
    return visitor.models
