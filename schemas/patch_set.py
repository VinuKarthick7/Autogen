from pydantic import BaseModel
from schemas.patch_operation import PatchOperation

class PatchSet(BaseModel):
    operations: list[PatchOperation]
