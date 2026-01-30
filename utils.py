from datetime import datetime


def parse_time(ts: str) -> datetime:
    return datetime.fromisoformat(ts)


def is_overlap(a_start, a_end, b_start, b_end) -> bool:
    return not (a_end <= b_start or b_end <= a_start)
