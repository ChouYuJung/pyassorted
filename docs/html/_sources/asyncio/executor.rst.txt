asyncio.executor
================

run_func
--------

.. autofunction:: pyassorted.asyncio.executor.run_func

Example code:

.. code-block:: python

    import asyncio
    from pyassorted.asyncio import run_func

    def normal_func() -> bool:
        return True

    async def async_func() -> bool:
        await asyncio.sleep(0.0)
        return True

    async main():
        assert await run_func(normal_func) is True
        assert await run_func(async_func) is True

    asyncio.run(main())
