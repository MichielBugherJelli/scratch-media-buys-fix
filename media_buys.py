"""Helpers for resolving media buy list filters.

The API contract for `get_media_buys` is subtle in list mode: when callers do
not provide `media_buy_ids`, the default status filter is `['active']` unless the
caller explicitly passes a value for `status_filter`.
"""

from __future__ import annotations

from typing import Iterable, Sequence

VALID_STATUSES = {
    "pending_creatives",
    "pending_start",
    "active",
    "paused",
    "completed",
    "rejected",
    "canceled",
}


def resolve_status_filter(
    media_buy_ids: Sequence[str] | None,
    status_filter: Sequence[str] | str | None,
) -> list[str] | None:
    """Resolve the effective status filter for get_media_buys list calls.

    Rules:
      - if `media_buy_ids` is provided, it takes precedence and no implicit list
        default is applied.
      - if `media_buy_ids` is omitted and `status_filter` is omitted, default to
        `['active']`.
      - if `status_filter` is explicitly supplied, use it as-is.
      - an empty list is invalid and raises ValueError to match schema constraints.
    """
    if media_buy_ids is not None:
        if status_filter == []:
            raise ValueError("status_filter cannot be empty")
        return list(status_filter) if status_filter is not None else None

    if status_filter == []:
        raise ValueError("status_filter cannot be empty")

    if status_filter is None:
        return ["active"]

    if isinstance(status_filter, str):
        status_filter = [status_filter]

    return list(status_filter)


def filter_media_buys(
    buy_records: Iterable[dict],
    media_buy_ids: Sequence[str] | None = None,
    status_filter: Sequence[str] | str | None = None,
    indicator_types: Sequence[str] | None = None,
) -> list[dict]:
    """Apply the list-mode filter rules and optional indicator composition."""
    effective_status_filter = resolve_status_filter(media_buy_ids, status_filter)

    matches: list[dict] = []
    indicator_types = tuple(indicator_types or ())

    for record in buy_records:
        if media_buy_ids is not None:
            if record.get("id") not in set(media_buy_ids):
                continue

        if effective_status_filter is not None:
            if record.get("status") not in effective_status_filter:
                continue

        if indicator_types and record.get("indicator_type") not in indicator_types:
            continue

        matches.append(record)

    return matches
