import pytest
from owui_client.models.evaluations import UpdateConfigForm, LeaderboardResponse
from owui_client.models.feedbacks import (
    FeedbackForm,
    RatingData,
    MetaData,
    ModelHistoryResponse,
)

pytestmark = pytest.mark.asyncio


async def test_evaluations_client_initialization(client):
    assert client.evaluations is not None


async def test_evaluations_config(client):
    # 1. Get config
    config = await client.evaluations.get_config()
    assert "ENABLE_EVALUATION_ARENA_MODELS" in config

    # 2. Update config
    form = UpdateConfigForm(ENABLE_EVALUATION_ARENA_MODELS=True)
    updated_config = await client.evaluations.update_config(form)
    assert updated_config["ENABLE_EVALUATION_ARENA_MODELS"] is True

    # Reset
    form = UpdateConfigForm(ENABLE_EVALUATION_ARENA_MODELS=False)
    await client.evaluations.update_config(form)


async def test_feedback_lifecycle(client):
    # 1. Create feedback
    feedback_form = FeedbackForm(
        type="rating",
        data=RatingData(rating=5, comment="Great!"),
        meta=MetaData(tags=["test"]).model_dump(),
        snapshot=None,
    )
    created_feedback = await client.evaluations.create_feedback(feedback_form)
    assert created_feedback is not None
    assert created_feedback.id is not None
    feedback_id = created_feedback.id

    # 2. Get feedback by ID
    feedback = await client.evaluations.get_feedback(feedback_id)
    assert feedback.id == feedback_id
    # FeedbackModel.data is dict; RatingData was stored as a dict in the JSON column.
    assert feedback.data["rating"] == 5

    # 3. Update feedback
    update_form = FeedbackForm(
        type="rating",
        data=RatingData(rating=4, comment="Good"),
    )
    updated_feedback = await client.evaluations.update_feedback(
        feedback_id, update_form
    )
    assert updated_feedback.data["rating"] == 4

    # 4. Get all feedback IDs (admin). In 0.10.1 GET /feedbacks/all was removed;
    # /feedbacks/all/ids returns FeedbackIdResponse items.
    all_ids = await client.evaluations.get_all_feedback_ids()
    assert len(all_ids) > 0
    found = any(f.id == feedback_id for f in all_ids)
    assert found

    # 5. Get user feedbacks (returns FeedbackListResponse: items + total)
    user_feedbacks = await client.evaluations.get_feedbacks_by_user()
    assert user_feedbacks.total > 0
    found_user = any(f.id == feedback_id for f in user_feedbacks.items)
    assert found_user

    # 6. Export feedbacks (GET /feedbacks/all/export -> list[FeedbackModel])
    export = await client.evaluations.export_all_feedbacks()
    assert len(export) > 0

    # 7. Get feedbacks list
    feedbacks_list = await client.evaluations.get_feedbacks_list(page=1)
    assert feedbacks_list.total > 0

    # 8. Delete feedback
    success = await client.evaluations.delete_feedback(feedback_id)
    assert success is True

    # Verify deletion (404 on subsequent get)
    from httpx import HTTPStatusError

    try:
        await client.evaluations.get_feedback(feedback_id)
        assert False, "Should have raised 404"
    except HTTPStatusError as e:
        assert e.response.status_code == 404


async def test_get_leaderboard(client):
    """Test the leaderboard endpoint returns a valid response."""
    leaderboard = await client.evaluations.get_leaderboard()
    assert leaderboard is not None
    assert isinstance(leaderboard, LeaderboardResponse)
    assert hasattr(leaderboard, "entries")
    assert isinstance(leaderboard.entries, list)


async def test_get_leaderboard_with_query(client):
    """Test the leaderboard endpoint with a query parameter."""
    leaderboard = await client.evaluations.get_leaderboard(query="coding")
    assert leaderboard is not None
    assert isinstance(leaderboard, LeaderboardResponse)
    assert hasattr(leaderboard, "entries")


async def test_get_model_history(client):
    """Test the model history endpoint."""
    # Create arena-style feedback for testing history
    # The leaderboard uses feedbacks with model_id, sibling_model_ids, and rating (1/-1)
    feedback_form = FeedbackForm(
        type="rating",
        data={
            "model_id": "test-model-history",
            "sibling_model_ids": ["opponent-model"],
            "rating": "1",  # Win
            "tags": ["test"],
        },
        meta={"arena": True},
        snapshot=None,
    )
    created = await client.evaluations.create_feedback(feedback_form)
    assert created is not None

    try:
        # Get model history
        history = await client.evaluations.get_model_history(
            "test-model-history", days=30
        )
        assert history is not None
        assert isinstance(history, ModelHistoryResponse)
        assert history.model_id == "test-model-history"
        assert hasattr(history, "history")
        assert isinstance(history.history, list)
    finally:
        # Cleanup
        await client.evaluations.delete_feedback(created.id)
