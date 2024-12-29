import asyncio
import time

def do_sleep():
    time.sleep(2)
    return "done"

async def main():
    # call do_sleep() three times concurrently
    # and wait for all of them to finish
    results = await asyncio.gather(
        asyncio.to_thread(do_sleep),
        asyncio.to_thread(do_sleep),
        asyncio.to_thread(do_sleep)
    )
    


if __name__ == "__main__":
    tic = time.time()
    asyncio.run(main())
    toc = time.time()
    
    print(f"Elapsed time: {toc - tic:.2f} seconds")