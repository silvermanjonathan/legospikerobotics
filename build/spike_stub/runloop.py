"""Stand-in for the SPIKE App 3 runloop module, used only by runcheck.py.

runloop.run takes the awaitable that calling main() returns, as in the SPIKE App:
runloop.run(main()).
"""
import asyncio
import motor_pair


def run(*functions):
    for f in functions:
        assert asyncio.iscoroutine(f), "runloop.run needs main(), with the brackets"
        asyncio.run(f)
    motor_pair.dump()
