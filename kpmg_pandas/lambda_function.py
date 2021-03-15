import json
from decimal import Decimal
import pandas as pd

DATASET_LINK = 'https://kpmg-project.s3.amazonaws.com/dataset.csv'


class CustomJSONEncoder(json.JSONEncoder):
    """ Tratamento de tipos de dados.
        Decimal para int ou float, set para list.
    """

    def default(self, o):
        if isinstance(o, Decimal):
            o_int = int(o)
            if o == o_int:
                return o_int
            return float(o)
        if isinstance(o, set):
            return list(o)
        return super().default(o)


def respond(status, body=None, headers=None):
    response = {
        "statusCode": status,
    }
    if not headers:
        if type(body) in [dict, list]:
            headers = {"Content-Type": "application/json"}
    if headers:
        response["headers"] = headers
    if body:
        response["body"] = json.dumps(body, cls=CustomJSONEncoder)
    return response


def lambda_handler(event, context):
    print(f'evento: {event}')
    path = event.get('path', "")
    print("path:", path)
    params = event.get('queryStringParameters', dict()) or {}
    if 'fabricantes' == path.split('/')[-1]:
        filtro = 'car_make'
    elif 'cidades' == path.split('/')[-1]:
        filtro = 'city'
    else:
        return respond(400, {"mensagem": f"caminho inválido"})

    try:
        data = get_data_dict(filtro)
        response = get_response(params, data)
        return response

    except Exception as e:
        print(f"Erro: {e}")
        return respond(500, {"mensagem": "Sistema temporariamente indisponível."})


def get_response(params, data):
    fabricante = params.get('fabricante') or None
    if fabricante:
        if fabricante in data:
            return respond(200, data.get(fabricante))
        else:
            return respond(400, {"mensagem": f"Fabricante {fabricante} não existe no banco de dados"})

    cidade = params.get('cidade') or None
    if cidade:
        if cidade in data:
            return respond(200, data.get(cidade))
        else:
            return respond(400, {"mensagem": f"Cidade {cidade} não existe no banco de dados"})

    return respond(200, data)


def get_data_dict(filtro):
    df = pd.read_csv(DATASET_LINK)
    df_media = df.groupby([filtro]).mean()['car_value']
    data = df_media.to_dict()
    return data
