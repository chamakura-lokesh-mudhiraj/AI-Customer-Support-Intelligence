from unittest.mock import Mock, patch

from app.services.embedding_service import create_embedding


def test_create_embedding():
    fake_response = Mock()

    fake_response.data = [
        Mock(
            embedding=[
                0.1,
                0.2,
                0.3,
                0.4,
            ]
        )
    ]

    with patch(
        "app.services.embedding_service.client.embeddings.create",
        return_value=fake_response,
    ) as mock_create:
        embedding = create_embedding(
            "Customers can request a refund within thirty days."
        )

    assert embedding == [0.1, 0.2, 0.3, 0.4]

    mock_create.assert_called_once_with(
        model="text-embedding-3-small",
        input="Customers can request a refund within thirty days.",
        encoding_format="float",
    )


def test_create_embedding_rejects_empty_text():
    try:
        create_embedding("")

        assert False
    except ValueError as exc:
        assert "Text cannot be empty." in str(exc)