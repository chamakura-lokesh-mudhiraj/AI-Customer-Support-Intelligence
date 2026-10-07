from unittest.mock import patch

import numpy as np
import pytest

from app.services.embedding_service import create_embedding


def test_create_embedding():
    fake_embedding = np.array(
        [
            0.1,
            0.2,
            0.3,
            0.4,
        ]
    )

    with patch(
        "app.services.embedding_service.model.encode",
        return_value=fake_embedding,
    ) as mock_encode:
        embedding = create_embedding("Test customer support ticket")

    assert embedding == [0.1, 0.2, 0.3, 0.4]

    mock_encode.assert_called_once_with(
        "Test customer support ticket",
        convert_to_numpy=True,
    )


def test_create_embedding_rejects_empty_text():
    with pytest.raises(ValueError, match="Text cannot be empty"):
        create_embedding("")