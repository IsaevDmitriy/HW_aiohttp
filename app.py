import pydantic
import aiopg
from aiohttp import web

password = ''
db = ''

PG_DSN = f'postgresql://{password}:1234@127.0.0.1:5432/{db}'


app = web.Application()


class UserSerializer(pydantic.BaseModel):
    username: str
    password: str



class HealthView(web.View):

    async def get(self):
        return web.json_response({'status': 'ok'})


    async def post(self):
        return web.json_response({'status': 'ok'})


class TestViewJson(web.View):

    async def post(self):
        json_data = await self.request.json()
        headers_data = dict(self.request.headers)
        return web.json_response({'json': json_data, 'headers': headers_data})


class TestViewVar(web.View):

    async def get(self):
        variable = self.request.match_info['test']
        return web.json_response({'variable': variable})


class User(web.View):

    async def post(self):
        user_data = await self.request.json()
        try:
            user_serialized = UserSerializer(**user_data)
            user_data = user_serialized.dict()

            return web.json_response(user_data)
        except pydantic.error_wrappers.ValidationError:

            raise web.HTTPBadRequest

    async def get(self):
        pool = self.request.app['pool']
        async with pool.accure() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT 1')
                response = await cursor.fetchall()
                return web.json_response({'response': response})



async def example_context(app):
    print(f'Старт')
    async with aiopg.create_pool(PG_DSN) as pool:
        app['pool'] = pool
        yield
        pool.close()
        print('Финиш')







app.add_routes([web.get('/health', HealthView)])
app.add_routes([web.post('/health', HealthView)])
app.add_routes([web.post('/json', TestViewJson)])
app.add_routes([web.get('/variable/{test}', TestViewVar)])
app.add_routes([web.post('/user', User)])
app.add_routes([web.get('/user', User)])
app.cleanup_ctx.append(example_context)

web.run_app(app, port=8080)