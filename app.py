import pydantic
import hashlib
from gino import Gino
from aiohttp import web
import sys
import asyncio


if sys.version_info[0] == 3 and sys.version_info[1] >= 8 and sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


password = ''
base = ''

PG_DSN = f'postgres://postgres:{password}@127.0.0.1:5432/{base}'


app = web.Application()
db = Gino()


class UserModel(db.Model):

    tablename = 'app_users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)

    _idx1 = db.Index('app_users_username', 'username', unique=True)




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
            user_data['password'] = hashlib.md5(user_data['password'].encode()).hexdigest()
            new_user = await UserModel.create(**user_data)

            return web.json_response(new_user.to_dict())
        except pydantic.error_wrappers.ValidationError:

            raise web.HTTPBadRequest


    async def get(self):
        user_id = self.request.match_info['user_id']
        user = await UserModel.get(int(user_id))
        user_data = user.to_dict()
        user_data.pop('password')
        return web.json_response(user_data)



async def init_orm(app):
    print(f'Старт')
    await db.set_bind(PG_DSN)
    await db.gino.create_all()
    yield
    await db.pop_bind().close
    print('Финиш')







app.add_routes([web.get('/health', HealthView)])
app.add_routes([web.post('/health', HealthView)])
app.add_routes([web.post('/json', TestViewJson)])
app.add_routes([web.get('/variable/{test}', TestViewVar)])
app.add_routes([web.post('/user', User)])
app.add_routes([web.get('/user/{int:user_id}', User)])

app.cleanup_ctx.append(init_orm)

web.run_app(app, port=8080)