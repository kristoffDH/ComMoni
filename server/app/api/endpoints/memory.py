from fastapi import APIRouter

from schemas.memory import Memory

router = APIRouter()


@router.post("/")
def create_disk(memory_data: Memory) -> Memory:
    return memory_data
