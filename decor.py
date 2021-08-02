


def print_decorator(coro):

    async def print_func(*args, **kwargs):

        print(f'Вызвана функция {coro.__name__}')
        print(f'Переменные {args} {kwargs}')
        result = await coro(*args, **kwargs)
        print(f'Result - {result}')
        return result

    return print_func


