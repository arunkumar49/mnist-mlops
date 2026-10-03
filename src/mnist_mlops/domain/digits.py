"""Core concepts for handwritten-digit classification."""

from __future__ import annotations

import math
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Final

from mnist_mlops.domain.errors import InvalidDigitError, InvalidProbabilitiesError

NUM_CLASSES: Final = 10
PROBABILITY_SUM_TOLERANCE: Final = 1e-6


@dataclass(frozen=True, slots=True)
class DigitLabel:
    """A digit class from 0 to 9. Invalid values cannot be constructed."""

    value: int

    def __post_init__(self) -> None:
        # bool is a subclass of int in Python, so True would otherwise pass as 1.
        if isinstance(self.value, bool) or not isinstance(self.value, int):
            raise InvalidDigitError(f"digit must be an int, got {type(self.value).__name__}")
        if not 0 <= self.value < NUM_CLASSES:
            raise InvalidDigitError(f"digit must be in 0..{NUM_CLASSES - 1}, got {self.value}")


@dataclass(frozen=True, slots=True)
class Prediction:
    """A model's probability distribution over the 10 digits."""

    probabilities: tuple[float, ...]

    def __post_init__(self) -> None:
        probs = self.probabilities
        if len(probs) != NUM_CLASSES:
            raise InvalidProbabilitiesError(
                f"expected {NUM_CLASSES} probabilities, got {len(probs)}"
            )
        if any(not math.isfinite(p) or p < 0.0 or p > 1.0 for p in probs):
            raise InvalidProbabilitiesError("every probability must be a finite number in [0, 1]")
        total = math.fsum(probs)
        if abs(total - 1.0) > PROBABILITY_SUM_TOLERANCE:
            raise InvalidProbabilitiesError(f"probabilities must sum to 1, got {total:.8f}")

    @classmethod
    def from_probabilities(cls, probabilities: Sequence[float]) -> Prediction:
        """Build a prediction from any sequence of numbers (list, tuple, array row)."""
        return cls(tuple(float(p) for p in probabilities))

    @property
    def label(self) -> DigitLabel:
        """The most likely digit. Ties resolve to the lowest digit, so results are deterministic."""
        best = max(range(NUM_CLASSES), key=lambda i: (self.probabilities[i], -i))
        return DigitLabel(best)

    @property
    def confidence(self) -> float:
        """Probability assigned to the predicted digit."""
        return self.probabilities[self.label.value]
