from typing import List, Optional

from .exceptions import ExceedsMaximumValueError, NegativeRangeError, NoMaximumValueError, NoMinimumValueError


class SmartRange:
    """
    SmartRange: A list of ranges.
    """

    ranges: List[range]

    def __init__(self, range_str: str, *, min_val: Optional[int] = None, max_val: Optional[int] = None):
        self.ranges = self._parse_range(range_str, min_val, max_val)

    def _parse_range(self, range_str: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> List[range]:
        parts = range_str.split(",")
        ranges = []
        locked_max = max_val
        current_max = min_val
        for part in parts:
            if not part.startswith("+"):
                start, sep, end = part.partition("-")
                start = int(start) if start else current_max
                if end:
                    end = int(end)
                else:
                    end = max_val
                    max_val = None
            else:
                start = current_max
                end = start + int(part[1:]) - 1
                # If we say +25, we want 25 numbers, not to end at the 25th index (26 numbers).
            if start is None:
                raise NoMinimumValueError(part)
            if end is None:
                raise NoMaximumValueError(part)
            if end < start:
                raise NegativeRangeError(start, end)
            if locked_max and max(start, end) > locked_max:
                raise ExceedsMaximumValueError(start, end, locked_max)
            ranges.append(range(start, end + 1))
            current_max = end + 1
        return ranges

    def __iter__(self):
        for r in self.ranges:
            yield from r

    def __len__(self):
        return sum(len(r) for r in self.ranges)

    def __contains__(self, item):
        return any(item in r for r in self.ranges)

    def __repr__(self):
        return ",".join(f"{r.start}-{r.stop - 1}" for r in self.ranges)
