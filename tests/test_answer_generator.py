from unittest.mock import Mock, patch

from app.services.answer_generator import generate_answer


def test_generate_answer():
    fake_response = Mock()
    fake_response.output_text = (
        "You can request a refund within thirty days."
    )

    with patch(
        "app.services.answer_generator.client.responses.create",
        return_value=fake_response,
    ) as mock_create:
        result = generate_answer(
            question="How long do I have to request a refund?",
            context=(
                "Customers can request a refund within thirty days."
            ),
            sources=["refund_policy.txt"],
        )

    assert result.answer == (
        "You can request a refund within thirty days."
    )

    assert result.sources == ["refund_policy.txt"]

    mock_create.assert_called_once()


def test_generate_answer_rejects_empty_question():
    try:
        generate_answer(
            question="",
            context="Some useful context.",
            sources=["test.txt"],
        )

        assert False
    except ValueError as exc:
        assert "Question cannot be empty." in str(exc)


def test_generate_answer_rejects_empty_context():
    try:
        generate_answer(
            question="What is the refund policy?",
            context="",
            sources=["test.txt"],
        )

        assert False
    except ValueError as exc:
        assert "Context cannot be empty." in str(exc)