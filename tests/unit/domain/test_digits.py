import math

import pytest

from mnist_mlops.domain.digits import NUM_CLASSES, DigitLabel, Prediction
from mnist_mlops.domain.errors import InvalidDigitError, InvalidProbabilitiesError


def one_hot(index: int) -> list[float]:
    return [1.0 if i == index else 0.0 for i in range(NUM_CLASSES)]


class TestDigitLabel:
    @pytest.mark.parametrize("value", [0, 5, 9])
    def test_accepts_digits(self, value: int) -> None:
        assert DigitLabel(value).value == value

    @pytest.mark.parametrize("value", [-1, 10, 255])
    def test_rejects_out_of_range(self, value: int) -> None:
        with pytest.raises(InvalidDigitError, match=r"must be in 0\.\.9"):
            DigitLabel(value)

    def test_rejects_bool(self) -> None:
        with pytest.raises(InvalidDigitError, match="must be an int"):
            DigitLabel(True)

    def test_rejects_float(self) -> None:
        with pytest.raises(InvalidDigitError, match="must be an int"):
            DigitLabel(3.0)  # type: ignore[arg-type]

    def test_is_immutable_and_comparable(self) -> None:
        assert DigitLabel(4) == DigitLabel(4)
        assert hash(DigitLabel(4)) == hash(DigitLabel(4))


class TestPrediction:
    def test_label_and_confidence(self) -> None:
        probs = [0.01] * NUM_CLASSES
        probs[7] = 1.0 - 0.01 * (NUM_CLASSES - 1)
        prediction = Prediction.from_probabilities(probs)
        assert prediction.label == DigitLabel(7)
        assert math.isclose(prediction.confidence, 0.91)

    def test_ties_resolve_to_lowest_digit(self) -> None:
        probs = [0.0] * NUM_CLASSES
        probs[3] = probs[8] = 0.5
        assert Prediction.from_probabilities(probs).label == DigitLabel(3)

    def test_accepts_tiny_float_rounding_error(self) -> None:
        probs = [0.1] * NUM_CLASSES  # sums to 0.9999999999999999 in floating point
        assert Prediction.from_probabilities(probs).label == DigitLabel(0)

    def test_rejects_wrong_length(self) -> None:
        with pytest.raises(InvalidProbabilitiesError, match="expected 10"):
            Prediction.from_probabilities([0.5, 0.5])

    @pytest.mark.parametrize("bad", [-0.1, 1.1, math.nan, math.inf])
    def test_rejects_invalid_values(self, bad: float) -> None:
        probs = one_hot(0)
        probs[1] = bad
        with pytest.raises(InvalidProbabilitiesError, match="finite number"):
            Prediction.from_probabilities(probs)

    def test_rejects_distribution_not_summing_to_one(self) -> None:
        with pytest.raises(InvalidProbabilitiesError, match="sum to 1"):
            Prediction.from_probabilities([0.2] * NUM_CLASSES)
