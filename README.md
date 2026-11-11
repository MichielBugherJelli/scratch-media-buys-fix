# Scratch Media Buys Fix

This repository captures the default list-mode behavior for `get_media_buys`:

- when `media_buy_ids` is omitted and `status_filter` is omitted, the effective
  filter is `['active']`.
- when `status_filter` is provided explicitly, it is respected as-is.
- when `media_buy_ids` is supplied, no implicit default status filter is applied.

The companion unit tests describe the expected behavior and verify the fix.
