from fastapi import APIRouter

from schemas.cpu import Cpu

router = APIRouter()


@router.post("/")
def create_cpu(cpu_data: Cpu) -> Cpu:
    return cpu_data
