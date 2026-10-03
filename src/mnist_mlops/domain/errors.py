"""Exceptions raised when a domain rule is broken."""


class DomainError(Exception):
    """Base class for every domain-rule violation."""


class InvalidDigitError(DomainError):
    """A label is not one of the digits 0-9."""


class InvalidProbabilitiesError(DomainError):
    """A probability vector is not a valid distribution over the 10 digits."""
