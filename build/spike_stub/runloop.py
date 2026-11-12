"""Stand-in for the SPIKE App 3 runloop module, used only by runcheck.py.

runloop.run takes the awaitable that calling main() returns, as in the SPIKE App:
runloop.run(main()). runloop.until(function) is awaitable and waits until the
function gives True. Here it asks the function up to POLLS times; if it never gives
True, the program is recorded as never getting past that line, which is what a robot
that drives on without stopping looks like.
"""
import asyncio
import motor_pair

POLLS = 200


class _Never(Exception):
    pass


async def until(function):
    assert callable(function), "runloop.until needs a function, such as a lambda"
    for _ in range(POLLS):
        if function():
            return
    motor_pair.CALLS.append({"call": "never"})
    raise _Never()


def run(*functions):
    for f in functions:
        assert asyncio.iscoroutine(f), "runloop.run needs main(), with the brackets"
        try:
            asyncio.run(f)
        except _Never:
            pass
    motor_pair.dump()
