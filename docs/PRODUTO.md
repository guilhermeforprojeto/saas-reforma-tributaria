# Do motor ao produto

A calculadora resolve **o cálculo**. Quem paga por um produto paga pelo resto: não precisar entender CST, `cClassTrib` e NCM; ver quanto o imposto muda; integrar com o que já usa; ter histórico para mostrar ao contador.

## Ideias, da mais simples à mais trabalhosa

| Ideia | Para quem | O que você constrói em volta da calculadora |
| --- | --- | --- |
| **Simulador de impacto da reforma** | Pequeno e médio empresário | Formulário simples (o que vende, quanto, onde) → quanto paga hoje × CBS/IBS de 2027 a 2033 → relatório em PDF para levar ao contador |
| **Classificador de produtos** | Lojas, indústrias, e-commerce | Importa a planilha de produtos, sugere CST/`cClassTrib` por NCM com as consultas de dados abertos, aponta itens sem vínculo (`REG-011`) para revisão |
| **API de cálculo gerenciada** | Software houses, ERPs pequenos | A calculadora hospedada, sempre atualizada, com chave de API, limite por plano, logs e SLA. O cliente não precisa manter Java nem acompanhar releases |
| **Plugin para emissor/ERP** | Quem usa Bling, Tiny, Omie, WooCommerce, Shopify… | Conector que pega o pedido, calcula, gera e valida o grupo XML e devolve para a nota |
| **Painel para escritórios de contabilidade** | Contadores com dezenas de clientes | Multi-cliente, lote de notas, conferência do que o cliente emitiu × o que a calculadora diz, alertas |

Antes de escolher, valide: rode o [`valide-antes-de-programar`](https://github.com/guilhermeforprojeto/valide-antes-de-programar) com a ideia e procure quem já faz o mesmo: o código está aberto para todo mundo, inclusive para os ERPs e emissores que o seu cliente já usa.

## Arquitetura mínima

```
Cliente (web / ERP / plugin)
        │ HTTPS, login ou chave de API
        ▼
Seu backend ── login, planos, limite de uso, cobrança, histórico, multi-cliente
        │ rede interna
        ▼
Calculadora da Receita (container, porta 8080 só interna, versão fixada)
```

- **Uma instância da calculadora atende muitos clientes:** ela não guarda estado (banco SQLite só de leitura). Escale com mais réplicas atrás de um balanceador.
- **Grave por cálculo:** cliente, entrada, saída, versão da calculadora, data.
- **Cache** das consultas de dados abertos (NCM, CST, classificações), que mudam pouco.
- **Atualização:** acompanhe as releases do repositório oficial. Suba a nova versão em homologação, rode os seus casos de teste (entradas reais anonimizadas com o resultado esperado) e só então troque em produção.

## Antes de vender

- **Responsabilidade:** deixe claro, nos termos e na tela, que o resultado é apoio ao cálculo e que a apuração é responsabilidade do contribuinte e do contador. Fale com um advogado sobre os termos.
- **Contador no time ou como parceiro:** para validar casos, escrever o conteúdo e dar credibilidade.
- **LGPD:** dados de notas e clientes são sensíveis; contrato de tratamento de dados, isolamento por cliente, exclusão a pedido.
- **Marca:** o código é MIT, mas o produto é seu. Não use o brasão nem dê a entender que é um serviço oficial.
- **Segurança:** revisão antes de abrir ([`revisao-de-seguranca-com-ia`](https://github.com/guilhermeforprojeto/revisao-de-seguranca-com-ia)), com foco em isolamento entre clientes.
- **Concorrência gratuita:** existe o simulador online oficial. O seu produto precisa ganhar em facilidade, integração ou volume.
