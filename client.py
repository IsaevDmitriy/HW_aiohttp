import aiohttp
import asyncio
from decor import print_decorator


HOST = 'http://127.0.0.1:8080'


@print_decorator
async def make_request(path, method='get', **kwargs):
    async with aiohttp.ClientSession() as session:
        request_method = getattr(session, method)
        async with request_method(f'{HOST}/{path}', **kwargs) as response:
            print(response.status)
            return (await response.text())



async def main():
    # response = await make_request('variable/hello_word')
    # response = await make_request('json', 'post', json={'123': '345'})
    # response = await make_request('user', 'post', json={'username': 'kos', 'password': 'ttt'})
    # response = await make_request('user', 'post', json={'user': 'kos', 'password': 'ttt'})
    # response = await make_request('user', 'get')
    response = await make_request('user', 'post', json={'username': 'nik', 'password': 'iii'})
    # await make_request('user/1', 'get')
    print(response)



asyncio.run(main())