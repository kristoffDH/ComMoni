from fastapi import APIRouter

from schemas.disk import Disk

router = APIRouter()


@router.post("/")
def create_disk(disk_data: Disk) -> Disk:
    return disk_data
