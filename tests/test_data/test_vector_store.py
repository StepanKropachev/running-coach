import numpy as np
import pytest

from data.vector_store.local import ChromaStore


@pytest.fixture
async def store():
    """Create a fresh in-memory store for each test."""
    store = ChromaStore(collection_name="test_collection")
    yield store
    await store.clear()


@pytest.mark.asyncio
async def test_add_and_get(store):
    # Test with numpy array
    embedding = np.array([1.0, 2.0, 3.0])
    metadata = {"type": "workout", "date": "2024-01-01"}

    id = await store.add(embedding, metadata)
    result = await store.get(id)

    assert len(result["embedding"]) == 3
    assert np.allclose(result["embedding"], embedding)
    assert result["metadata"] == metadata


@pytest.mark.asyncio
async def test_add_many(store):
    embeddings = [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]]
    metadata = [
        {"type": "workout", "date": "2024-01-01"},
        {"type": "workout", "date": "2024-01-02"},
    ]

    ids = await store.add_many(embeddings, metadata)
    assert len(ids) == 2

    for id in ids:
        result = await store.get(id)
        assert len(result["embedding"]) == 3


@pytest.mark.asyncio
async def test_update(store):
    embedding = [1.0, 2.0, 3.0]
    metadata = {"type": "workout", "date": "2024-01-01"}

    id = await store.add(embedding, metadata)

    new_metadata = {"type": "workout", "date": "2024-01-02"}
    await store.update(id, metadata=new_metadata)

    result = await store.get(id)
    assert result["metadata"] == new_metadata


@pytest.mark.asyncio
async def test_delete(store):
    id = await store.add([1.0, 2.0, 3.0])
    await store.delete(id)

    with pytest.raises(KeyError):
        await store.get(id)


@pytest.mark.asyncio
async def test_search(store):
    # Add some test data
    embeddings = [
        [1.0, 0.0, 0.0],  # Close to query
        [0.0, 1.0, 0.0],  # Further from query
        [0.0, 0.0, 1.0],  # Further from query
    ]
    metadata = [{"type": "A"}, {"type": "B"}, {"type": "A"}]

    await store.add_many(embeddings, metadata)

    # Search with vector closest to first embedding
    query = [0.9, 0.1, 0.0]
    results = await store.search(query, limit=2)

    assert len(results) == 2
    assert np.allclose(
        results[0]["embedding"], [1.0, 0.0, 0.0]
    )  # Closest should be first


@pytest.mark.asyncio
async def test_search_with_filter(store):
    embeddings = [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]
    metadata = [{"type": "A"}, {"type": "B"}]

    await store.add_many(embeddings, metadata)

    results = await store.search([1.0, 0.0, 0.0], metadata_filter={"type": "B"})

    assert len(results) == 1
    assert results[0]["metadata"]["type"] == "B"


@pytest.mark.asyncio
async def test_clear(store):
    await store.add([1.0, 2.0, 3.0])
    await store.clear()

    # Search should return empty results
    results = await store.search([1.0, 2.0, 3.0])
    assert len(results) == 0
