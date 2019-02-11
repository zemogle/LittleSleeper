import asyncio
import websockets
import json
import aiohttp


try:
    import unicornhathd
    print("unicorn hat hd detected")
except ImportError:
    from unicorn_hat_sim import unicornhathd


async def communicate(loop):
    tmp = 0
    # async with websockets.connect('ws://localhost:5678') as websocket:
    #         while True:
    #             data = await websocket.recv()
    #             colours = json.loads(data)
    #             for i, colour in enumerate(colours):
    #                 x, y = divmod(i, 16)
    #                 unicornhathd.set_pixel(x, y, colour[0], colour[1], colour[2])
    #             unicornhathd.show()
    #             await asyncio.sleep(5, loop=loop)
    async with aiohttp.ClientSession() as session:
        async with session.ws_connect('ws://localhost:5678') as ws:
            async for msg in ws:
                while True:
                    tmp += 1
                    colours = json.loads(msg.data)
                    for i, colour in enumerate(colours):
                        x, y = divmod(i, 16)
                        unicornhathd.set_pixel(x, y, colour[0], colour[1], colour[2])
                    unicornhathd.show()
                    if msg.type == aiohttp.WSMsgType.TEXT:
                        if msg.data == 'close cmd':
                            await ws.close()
                            break
                    elif msg.type == aiohttp.WSMsgType.ERROR:
                        break
                    await asyncio.sleep(1)
                    print(tmp)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(communicate(loop))


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        unicornhathd.off()
        # pass
