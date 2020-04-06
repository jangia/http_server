import asyncio
import time

from aiohttp import ClientSession


async def hello(fetch_url):
    async with ClientSession() as session:
        async with session.get(fetch_url) as response:
            response = await response.read()
            print(response)


def main():
    loop = asyncio.get_event_loop()

    tasks = []

    url = "http://localhost:8000"
    for i in range(1000):
        task = asyncio.ensure_future(hello(url.format(i)))
        tasks.append(task)
    loop.run_until_complete(asyncio.wait(tasks))


if __name__ == '__main__':
    start = time.time()
    main()
    stop = time.time()
    print(f'It took: {stop - start} seconds.')

