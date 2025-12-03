import pytest
from owui_client.models.evaluations import UpdateConfigForm
from owui_client.models.feedbacks import (
    FeedbackForm,
    RatingData,
    MetaData,
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
    # Rating might be returned as dict or obj depending on how backend stores it in JSON column
    # The model says data is Optional[dict]. The client model parses it.
    # But RatingData is a pydantic model.
    # FeedbackModel.data is dict.
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

    # 4. Get all feedbacks (admin)
    all_feedbacks = await client.evaluations.get_all_feedbacks()
    assert len(all_feedbacks) > 0
    found = any(f.id == feedback_id for f in all_feedbacks)
    assert found

    # 5. Get user feedbacks
    user_feedbacks = await client.evaluations.get_feedbacks_by_user()
    assert len(user_feedbacks) > 0
    found_user = any(f.id == feedback_id for f in user_feedbacks)
    assert found_user

    # 6. Export feedbacks
    export = await client.evaluations.export_all_feedbacks()
    assert len(export) > 0

    # 7. Get feedbacks list
    feedbacks_list = await client.evaluations.get_feedbacks_list(page=1)
    assert feedbacks_list.total > 0

    # 8. Delete feedback
    success = await client.evaluations.delete_feedback(feedback_id)
    assert success is True

    # Verify deletion
    try:
        await client.evaluations.get_feedback(feedback_id)
        assert False, "Should have raised 404"
    except Exception:
        pass

