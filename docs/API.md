# API da calculadora: o essencial

Resumo do que está no repositório oficial ([README](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular) e [`docs/exemplos.md`](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular/blob/main/docs/exemplos.md)) e no [guia de integração com ERP](https://piloto-cbs.tributos.gov.br/servico/calculadora-consumo/calculadora/documentacao/guia-integracao). A lista completa, com esquemas, fica no Swagger da sua instância: `http://localhost:8080/api/swagger-ui.html`.

Base: `http://localhost:8080/api/calculadora`

## Endpoints principais

| O quê | Método e caminho |
| --- | --- |
| Calcular a operação (falha inteira no primeiro erro, HTTP 422) | `POST /regime-geral` |
| Calcular item a item (erro por item, HTTP 200) | `POST /observabilidade/regime-geral` |
| Explicar um código de erro | `GET /observabilidade/erros?codigo=REG-011` |
| Base de cálculo unificada NF-e/NFC-e | `POST /base-calculo/base-calculo-unificada` |
| Base de cálculo unificada NFS-e | `POST /base-calculo/base-calculo-unificada-nfse` |
| Gerar o XML do grupo de tributação | `POST /xml/generate?tipo=nfe` |
| Validar XML contra o XSD | `POST /xml/validate?tipo=nfe&subtipo=grupo` (ou `nota`) |
| CST e classificação tributária | `GET /dados-abertos/situacoes-tributarias/cbs-ibs`, `GET /dados-abertos/classificacoes-tributarias/...` |
| Fundamentação legal | `GET /dados-abertos/fundamentacoes-legais` |
| NCM e NBS | `GET /dados-abertos/ncm`, `GET /dados-abertos/nbs` |
| Alíquotas de referência | `GET /dados-abertos/aliquota-uniao`, `/aliquota-uf`, `/aliquota-municipio` |
| Versão | `GET /dados-abertos/versao` |

## O fluxo de uma nota

O guia oficial de integração com ERP tem 4 passos:

1. **Calcular** → `POST /regime-geral`
2. **Gerar o XML** dos grupos de tributação com a resposta do passo 1 → `POST /xml/generate`
3. **Validar** o XML → `POST /xml/validate`
4. **Injetar** o grupo no XML do documento fiscal que o seu sistema já monta (NF-e, NFC-e, NFS-e)

O passo 2 usa a resposta de `/regime-geral`, não a da observabilidade.

## Entrada

Exemplo completo em [`../exemplos/operacao.json`](../exemplos/operacao.json) (tirado do repositório oficial). Campos de cada operação:

- `id`, `versao`, `dhFatoGerador` (ISO 8601 com fuso), `municipio` (código IBGE), `uf`
- `itens[]`: `numero`, `ncm` (bens) **ou** `nbs` (serviços), `cst`, `cClassTrib`, `baseCalculo`, `quantidade`, `unidade`
- `aliquotasNominais` (`cbs`, `ibsEstadual`, `ibsMunicipal`, e `impostoSeletivo` quando houver): **obrigatório a partir de 2027, proibido antes**
- `impostoSeletivo` no item, quando o produto tem IS

## Saída

- `objetos[]`: um por item, com `estadoItem` e `tribCalc` (grupos `IBSCBS` e `IS`, com base, alíquota, redução e valor) ou `erros[]` (`code`, `title`, `pointer`, `detail`)
- `total.tribCalc`: `ISTot` e `IBSCBSTot` (somam só os itens calculados)
- Cada grupo traz `memoriaCalculo` em texto: guarde e mostre ao usuário

Estados de item: `CALCULADO`, `CALCULO_SIMULADO`, `INCONSISTENCIA_ENTRADA`, `NAO_IMPLEMENTADO`, `FALHA_TECNICA`.

## Pegadinhas

- Resposta 200 na observabilidade **não** quer dizer que tudo foi calculado.
- `CALCULO_SIMULADO` + header `x-warning-dados-simulados`: o cálculo usou alíquotas informadas por você.
- Consulta de alíquota de referência para 2027 em diante retorna 404: elas precisam vir em `aliquotasNominais`.
- Base unificada: em 2027, PIS e COFINS são ignorados (com aviso); ICMS e FCP ainda são deduzidos.
- NCM precisa estar vinculada à `cClassTrib` (erro `REG-011`). Use as consultas de dados abertos para montar listas de escolha no seu produto.

## Outras calculadoras da Receita

- [calculadora-rtc-simples-nacional](https://github.com/ReceitaFederal/calculadora-rtc-simples-nacional): CBS e IBS de optantes do Simples Nacional.
- [calculadora-rtc-gerador-danfse](https://github.com/ReceitaFederal/calculadora-rtc-gerador-danfse): gera o PDF do DANFSe a partir do XML da NFS-e (Go).
