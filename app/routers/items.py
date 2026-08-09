from fastapi import APIRouter, HTTPException, status

from app.schemas.item import ItemCreate, ItemResponse, ItemUpdate

router = APIRouter()

# In-memory store for demo purposes
_items: dict[int, ItemResponse] = {}
_next_id = 1


@router.get("", response_model=list[ItemResponse])
def list_items() -> list[ItemResponse]:
    return list(_items.values())


@router.get("/{item_id}", response_model=ItemResponse)
def get_item(item_id: int) -> ItemResponse:
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    return item


@router.post("", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(payload: ItemCreate) -> ItemResponse:
    global _next_id
    item = ItemResponse(id=_next_id, **payload.model_dump())
    _items[_next_id] = item
    _next_id += 1
    return item


@router.put("/{item_id}", response_model=ItemResponse)
def update_item(item_id: int, payload: ItemUpdate) -> ItemResponse:
    item = _items.get(item_id)
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    updated = item.model_copy(update=payload.model_dump(exclude_unset=True))
    _items[item_id] = updated
    return updated


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int) -> None:
    if item_id not in _items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    del _items[item_id]
