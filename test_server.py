"""Quick self-check: python test_server.py"""

import asyncio

from mcp.server.mcpserver.exceptions import ToolError
from server import get_booking, list_bookings, occupancy, search_faq, server

assert get_booking(" b003 ")["pet"] == "Rocket"
try:
    get_booking("B999")
    raise AssertionError("expected ToolError")
except ToolError:
    pass

assert len(list_bookings()) == 15
assert all(b["status"] == "pending" for b in list_bookings("Pending"))
try:
    list_bookings("all")
    raise AssertionError("expected ToolError")
except ToolError:
    pass

# B001 checks out 11-17, so it is not counted that night; B005 is cancelled.
o = occupancy("2026-11-17")
assert "B001" not in o["booking_ids"] and "B005" not in o["booking_ids"]
assert o["booking_ids"] == ["B003", "B004", "B006"], o
assert o["count"] == o["dogs"] + o["cats"]
try:
    occupancy("next friday")
    raise AssertionError("expected ToolError")
except ToolError:
    pass

assert search_faq("vaccines for my dog")[0]["question"].startswith("What vaccinations")
assert search_faq("zzz") == []

# The server really registers the four tools, marked read-only.
tools = asyncio.run(server.list_tools())
assert sorted(t.name for t in tools) == ["get_booking", "list_bookings", "occupancy", "search_faq"]
assert all(t.annotations.read_only_hint for t in tools)

print("all checks passed")
