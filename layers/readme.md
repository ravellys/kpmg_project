# AWS Lambda Layers

Como criar novos pacotes para usar como layer de funções AWS Lambda.  
[Docs](https://docs.aws.amazon.com/lambda/latest/dg/configuration-layers.html)

## Installation

Criar um diretório com nome "python" e instalar o pacote neste diretório.

```bash
mkdir python
python3.x -m pip install -t "python/" <packagename>
# Exemplo:
# python3.8 -m pip install -t "python/" requests
```

Remover cache (reduz o tamanho final do pacote)
```bash
find . -regex '^.*\(__pycache__\|\.py[co]\)$' -delete
```

Instalar dependência, caso necessário
```bash
sudo apt install zip unzip
```

Compactar o conteúdo em um arquivo .zip
```bash

# Criar arquivo zip
zip -r <packagename>-<packageversion>_py3x.zip python/
# Exemplo:
# zip -r requests-2.24.0_py38.zip python/
```
