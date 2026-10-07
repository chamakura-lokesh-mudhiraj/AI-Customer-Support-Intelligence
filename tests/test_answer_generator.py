from unittest.mock import Mock, patch

import pytest

from app.services.answer_generator import generate_answer


def test_generate_answer():
    fake_response = Mock()

    fake_response.json.return_value = {
        "response": (
            "You can request a refund within thirty days."
        )
    }

    with patch(
        "app.services.answer_generator.requests.post",
        return_value=fake_response,
    ) as mock_post:
        fake_response.raise_for_status.return_value = None

        result = generate_answer(
            question="How long do I have to request a refund?",
            context=(
                "Customers can request a refund within "
                "30 days of the original purchase."
            ),
            sources=["refund_policy.txt"],
        )

    assert result.answer == (
        "You can request a refund within thirty days."
    )

    assert result.sources == ["refund_policy.txt"]

    mock_post.assert_called_once()

    request_body = mock_post.call_args.kwargs["json"]

    assert request_body["model"] == "mistral:latest"
    assert "How long do I have to request a refund?" in (
        request_body["prompt"]
    )


def test_generate_answer_rejects_empty_question():
    with pytest.raises(
        ValueError,
        match="Question cannot be empty",
    ):
        generate_answer(
            question="",
            context="Some context",
            sources=["refund_policy.txt"],
        )


def test_generate_answer_rejects_empty_context():
    with pytest.raises(
        ValueError,
        match="Context cannot be empty",
    ):
        generate_answer(
            question="What is the refund policy?",
            context="",
            sources=["refund_policy.txt"],
        )