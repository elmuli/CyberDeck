import keyboardTest_Cpy as kb
import ActualCodeMouse as mu
import asyncio

async def main():
    await asyncio.gather(
        mu.Main(),
        kb.Main()
    )
    
asyncio.run(main())
    