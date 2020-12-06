import logging
import sys
import asyncio
from simpervisor.process import SupervisedProcess

async def main():
    proc = SupervisedProcess('test', sys.executable, 'test.py')
    await proc.start()


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s %(msg)s', level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    try:
        asyncio.ensure_future(main())
        loop.run_forever()
    finally:
        loop.run_until_complete(asyncio.gather(*asyncio.Task.all_tasks()))
        loop.close()