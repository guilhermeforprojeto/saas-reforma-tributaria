# AGENTS.md — SaaS em cima da Calculadora da Reforma Tributária

Você (IA) recebeu o link deste repositório. Ele ensina a usar a **Calculadora de Tributos da Receita Federal** (código aberto, licença MIT, em [ReceitaFederal/calculadora-rtc-regime-regular](https://github.com/ReceitaFederal/calculadora-rtc-regime-regular)) como motor de cálculo de um produto: SaaS, módulo de ERP, API ou ferramenta interna.

Responda no idioma do usuário.

## Primeiro: o que o usuário quer?

Pergunte uma vez (pule se ele já disse):

1. **Só rodar a calculadora** na máquina para testar → siga "Rodar a calculadora".
2. **Integrar num sistema que já existe** (ERP, emissor de nota, e-commerce) → "Rodar" + [`docs/API.md`](docs/API.md) + passo 4 abaixo.
3. **Criar um produto novo** → "Rodar" + [`docs/PRODUTO.md`](docs/PRODUTO.md). Antes de codar, sugira validar a ideia com o [`valide-antes-de-programar`](https://github.com/guilhermeforprojeto/valide-antes-de-programar).

## Rodar a calculadora

Peça permissão antes de instalar qualquer coisa. Dois caminhos:

**A. Docker (recomendado, não precisa de Java):**

```bash
git clone https://github.com/guilhermeforprojeto/saas-reforma-tributaria.git
cd saas-reforma-tributaria
docker compose -f docker/docker-compose.yml up -d --build
```

O build clona o código oficial, gera o banco de tabelas e compila. Leva alguns minutos na primeira vez.

**B. Direto do código oficial (precisa de Java 25+):**

```bash
git clone https://github.com/ReceitaFederal/calculadora-rtc-regime-regular.git
cd calculadora-rtc-regime-regular
mkdir -p ./calculadora/db
./mvnw flyway:migrate -Dflyway.configFiles=./flyway/flyway-pro.conf --batch-mode --errors
./mvnw spring-boot:run -Dspring-boot.run.profiles=offline
```

No Windows: `mvnw.cmd` e `mkdir calculadora\db`. O banco é obrigatório: sem o passo do `flyway:migrate`, a aplicação não sobe.

**Conferir:** `http://localhost:8080/api/calculadora/dados-abertos/versao` responde, e o Swagger abre em `http://localhost:8080/api/swagger-ui.html`. Depois rode `bash exemplos/calcular.sh` ou `python exemplos/calcular.py`: o item 4 do exemplo tem erro de propósito (`REG-011`).

## Regras ao construir em cima dela

1. **Não altere a regra de cálculo** do código oficial. O valor do produto vem justamente de usar o cálculo da Receita. Se achar um erro de cálculo, reporte no repositório oficial (issues) e não "corrija" localmente.
2. **A calculadora não tem login.** Nunca exponha a porta 8080 na internet. Ela roda como serviço interno, atrás do backend do produto, que cuida de login, limite de uso e cobrança.
3. **Fixe a versão** (tag/commit) em produção e registre em cada cálculo qual versão da calculadora foi usada. Atualize de propósito, lendo o `CHANGELOG.md` oficial e rodando os testes do produto.
4. **Trate o resultado item a item.** Use `POST /observabilidade/regime-geral` quando quiser cálculo parcial: a resposta é 200 mesmo com erro, então confira o `estadoItem` de cada item. `POST /regime-geral` falha a operação inteira (HTTP 422) no primeiro erro.
5. **Ano importa:** a partir de 2027, `aliquotasNominais` é obrigatório na entrada; antes disso, é proibido. Cálculos com alíquotas informadas voltam como `CALCULO_SIMULADO` com o header `x-warning-dados-simulados`. As alíquotas de referência da consulta de dados abertos existem só para 2026.
6. **Use `dhFatoGerador`,** não `dataHoraEmissao` (obsoleto).
7. **Guarde a entrada e a saída** de cada cálculo (com a memória de cálculo que a API devolve). É o que o cliente vai mostrar ao contador se houver dúvida.
8. **Aviso no produto:** o resultado é uma simulação/apoio ao cálculo e não substitui a análise de um contador. Não prometa "cálculo garantido pela Receita".
9. **Dados de clientes:** CNPJ, notas e valores são dados sensíveis. Isolamento por cliente, LGPD e revisão de segurança antes de lançar (veja [`revisao-de-seguranca-com-ia`](https://github.com/guilhermeforprojeto/revisao-de-seguranca-com-ia)).
10. **Licença:** o código da Receita é MIT (pode usar e vender, mantendo o aviso de copyright e a licença). Não use marcas, brasões ou o nome "Receita Federal" de forma que pareça produto oficial.

## O que você entrega

- A calculadora rodando e o exemplo passando, com prints ou saída do terminal.
- Se for integração: o código que monta a entrada a partir dos dados do sistema, chama a API, trata os estados e grava o resultado.
- Se for produto: o plano de [`docs/PRODUTO.md`](docs/PRODUTO.md) adaptado à ideia escolhida, e só então o código.
