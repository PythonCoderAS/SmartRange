class RangeError(ValueError):
    """Raised when a value is invalid."""
    pass


class NoValueExpectedError(RangeError):
    """Raised when a value is expected but none is provided."""
    pass


class NoMaximumValueError(NoValueExpectedError):
    """Raised when a range is specified that assumes a maximum value but none if specified."""

    string: str

    def __init__(self, string: str):
        self.string = string
        super().__init__(f"Range {string!r} specifies no end value but no maximum value was specified.")


class NoMinimumValueError(NoValueExpectedError):
    """Raised when a range is specified that assumes a minimum value but none if specified."""

    string: str

    def __init__(self, string: str):
        self.string = string
        super().__init__(f"Range {string!r} specifies no start value but no minimum value was specified.")


class ExceedsMaximumValueError(RangeError):
    """Raised when a value goes past the maximum."""

    @property
    def string(self) -> str:
        return f"{self.start}-{self.end}"

    start: int
    end: int
    max_value: int

    def __init__(self, start: int, end: int, max_value: int):
        self.start = start
        self.end = end
        self.max_value = max_value
        super().__init__(
            f"Value {self.string!r} exceeds the specified maximum value of the overall range ({max_value}).")


class NegativeRangeError(RangeError):
    """Raised when a range is specified that is negative."""

    start: int
    end: int

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end
        super().__init__(f"End value ({end}) is smaller than start value ({start}).")
