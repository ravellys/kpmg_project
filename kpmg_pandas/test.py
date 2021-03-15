import os
import time
import datetime
from lambda_function import lambda_handler


os.environ['aws_region'] = 'us-east-1'
event = {
    "path": "/valoresmedioscarros/cidades",
    "queryStringParameters": {"cidade": "C_01"},
}


class Context:
    pass

context = Context()


def timeit(method):
    def timed(*args, **kwargs):
        start_time = time.time()
        result = method(*args, **kwargs)
        elapsed_time = time.time() - start_time
        seconds = round(elapsed_time)
        idvarejista = kwargs.get('idvarejista')
        if elapsed_time >= 1:
            print(
                f"Tempo de execução ({method.__name__}): {datetime.timedelta(seconds=seconds)}{' (' + idvarejista + ')' if idvarejista else ''}")
        elif elapsed_time >= 0.01:
            print(
                f"Tempo de execução ({method.__name__}): {elapsed_time:.2f}s{' (' + idvarejista + ')' if idvarejista else ''}")
        return result

    return timed


@timeit
def run(metodo, **kwargs):
    return metodo(**kwargs)


kwargs = {
    'event': event,
    'context': context
}
print(run(lambda_handler, **kwargs))
