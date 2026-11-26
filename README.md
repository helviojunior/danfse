# danfse

Gerador da **DANFSe** (Documento Auxiliar da NFS-e Nacional) em **PDF** a partir
do **XML** da NFS-e, em Python.

Port para Python da biblioteca PHP
[`guilhermecfviana/danfse-nacional`](https://github.com/guilhermecfviana/danfse-nacional)
(MIT). Renderiza o leiaute oficial **DANFSe v2.0** via HTML + CSS com
[WeasyPrint](https://weasyprint.org/), com QR Code de consulta pública.

> Contexto: o serviço de geração de DANFSe (PDF) do gov.br foi descontinuado.
> Esta biblioteca gera o PDF localmente a partir do XML autorizado da nota.

## Instalação

```bash
pip install danfse
```

### Dependências de sistema (WeasyPrint)

O WeasyPrint precisa de bibliotecas nativas (Pango, cairo, gdk-pixbuf). Instale
conforme o sistema operacional:

```bash
# Debian / Ubuntu
sudo apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf-2.0-0 \
    libffi-dev libcairo2 fonts-liberation

# macOS (Homebrew)
brew install pango gdk-pixbuf libffi

# Fedora
sudo dnf install pango gdk-pixbuf2 cairo liberation-sans-fonts
```

Para melhor fidelidade visual, instale as fontes **Liberation Sans**
(metric-compatíveis com Arial). Veja a documentação oficial do WeasyPrint para
detalhes por plataforma.

## Uso

### Python

```python
from danfse import generate

# Autodetecta: caminho de arquivo, string XML ou bytes XML
pdf = generate("nota.xml")

with open("danfse.pdf", "wb") as fh:
    fh.write(pdf)
```

Funções específicas e opções:

```python
from danfse import generate_from_file, generate_from_string, Options

generate_from_file("nota.xml", Options(output="file", output_path="danfse.pdf"))

xml = open("nota.xml", "rb").read()
pdf = generate_from_string(xml, {"watermark": "cancelada"})  # dict também funciona
```

Opções (`Options`):

| campo         | valores                                   | descrição                                   |
|---------------|-------------------------------------------|---------------------------------------------|
| `output`      | `"bytes"` (padrão) \| `"file"`            | também grava em `output_path` quando `file` |
| `output_path` | caminho                                   | PDF de saída                                |
| `watermark`   | `None` \| `"cancelada"` \| `"substituida"`| marca d'água                                |
| `logo`        | caminho de imagem                         | substitui o logo padrão da NFS-e            |
| `footer_text` | texto                                     | rodapé repetido em todas as páginas         |

### CLI

```bash
danfse nota.xml                     # gera nota.pdf
danfse nota.xml -o danfse.pdf
danfse nota.xml --watermark cancelada
```

## Notas sobre o leiaute

- Notas em **homologação** (`tpAmb = 2`) recebem marca d'água "HOMOLOGAÇÃO" e o
  aviso "NFS-e SEM VALIDADE JURÍDICA".
- Grupos opcionais do leiaute (intermediário, destinatário, IBS/CBS) só são
  exibidos quando presentes no XML.
- O QR Code aponta para a consulta pública oficial:
  `https://www.nfse.gov.br/ConsultaPublica/?tpc=1&chave={chave}`.

## Desenvolvimento

```bash
pip install -e ".[dev]"
pytest
ruff check .
```

## Licença

MIT. Veja [LICENSE](LICENSE) e [NOTICE](NOTICE) (créditos ao projeto original e
aos dados/ativos de terceiros).
