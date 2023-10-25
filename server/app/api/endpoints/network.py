from fastapi import APIRouter

from schemas.network import Network

router = APIRouter()


@router.post("/")
def create_disk(network_data: Network) -> Network:
    return network_data
