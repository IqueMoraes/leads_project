# Leads Project

## Overview

Esta api tem como propósito o registro quantitativo de acesso dos usuários em sites ou aplicações, bem como, a leitura desses dados.
Seu funcionamento estará ligado ao banco de dados relacional suportado pela Heroku, que guardará os registros de acesso em nuvem.
Foi desenvolvida para compor informações sobre frequência identificando potenciais clientes e também abandono do serviço.

## Getting Started

Esta API oferece ao desenvolvedor uma forma simples de registrar acesso apenas com dado do e-mail cadastrado.
Poderá ser usada como melhor entender em seu projeto não demandando autenticação.
É indicado breve conhecimento sobre o uso de **leads** para que possa gerar suas próprias informações através dos dados fornecidos pela API.

### Warning

Em estrutura simples esta API não usa ferramentas de autenticação, portanto, as rotas não deverão ser fornecidas de forma pública.
O acesso por pessoas que não desenvolvedoras do projeto poderão gerar poluição e deleção dos dados comprometendo, assim, informações importantes aos objetivos dos profissionais envolvidos.

## Leads project API background:

### Leads concepts:

**Id** - Número gerado automaticamente de forma sequencial e nunca repetido para identificação de um usuário no banco de dados.

**name** - Nome do usuário para identificação em leitura dos dados.

**email** - Endereço eletrônico do usuário. Comumente usado em sites e aplicações para operações pelo usuário final, é fundamental nesta API para interação com banco de dados.

**phone** - Número de contato móvel do usuário em território brasileiro para chamada telefônica. Apresenta caracteres especiais para identificação da Discagem Direta à Distância (DDD).

**creation_date** - Data da inserção do usuário no banco de dados.

**last_visit** - Data da última atualização do usuário no banco de dados. Leia-se, data da última visita do usuário no site ou aplicação. Data atualizada via requisição.

**visits** - Número de visitas de um único usuário. Esse número será atualizado sempre em requisição.

## Leads API data model:

**Id** - Chave primária do usuário tipo inteiro e sequencial, gerada automaticamente, acrescida a cada requisição e nunca repetida. Não mutável.

**name** - Nome do usuário em tipo string, sem formatação e não podendo estar vazio. Não mutável.

**email** - Endereço eletrônico em tipo string, caracteres formatados em caixa baixa, porém sem checagem de condição de e-mail ("@", ".com", ".com.br", ...). Dado de caráter único em todo banco de dados e não poderá estar vazio. Não mutável.

**phone** - Número de contato do usuário em tipo string, não podendo estar vazio e sendo único. Dado não formatado, porém com checagem de dígitos e caracteres especiais.
Verifica-se o uso de parênteses, traço e números. Apresenta no formato **(00)11111-2222**. Não mutável.

**creation_date** - Data de registro do usuário no banco de dados gerado automaticamente. Tipo string fornecido pela biblioteca nativa da linguagem Python, _Datetime_ em região local. Não mutável.

**last_visit** - Data do último acesso do usuário. Inicialmente gerada automaticamente com a mesma data de registro do usuário. Posteriormente o valor é atualizado a cada requisição de update. Tipo string fornecido pela biblioteca nativa da linguagem Python, _Datetime_ em região local. Mutável.

**visits** - Número de visitas total do usuário. Tipo inteiro sendo iniciado em um(1). É acrescido do número um(1) a cada requisição de atualização. Mutável.

## Leads API operations

| Operation    | Description                                                                                                                                                                                        | REST HTTP                                                                                                              |
| ------------ | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------- |
| **Cria**     | Insere um novo usuário no banco de dados                                                                                                                                                           | Envia requisição **POST** com os dados não nulos do usuário.                                                           |
| **Lista**    | Entrega uma lista de todos os usuários em ordem descrescente dado pelo número de visitas.                                                                                                          | Sob requisição **GET** entrega uma lista dos usuários em formato de dicionário JSON.                                   |
| **Atualiza** | Atualiza a data da última visita do usuário com data, hora e minuto no momento do processamento do código. Atualiza o número de visitas acrescentando um ao número de visitas que tiver o usuário. | As alterações ocorrem automaticamente via requisição **PATCH** com campo obrigatório "email" no corpo em formato JSON. |
| **Apaga**    | Retira do banco de dados as informações do usuário. Não é recuperável. Não disponibiliza o número do id para um novo usuário.                                                                      | A requisição é feita com o método **DELETE** e com campo obrigatório "email" no corpo em formato JSON.                 |

## Data format

[JSON](https://developers.google.com/books/docs/v1/getting_started#data-json)

# Requests

URL de base: http://localhost/leads

**Nenhum método possui URL específica

## POST - insere novo usuário


Modelo do corpo da requisição:

> {<br/>
> "name": "John Doe dOe ",<br/>
> "email": "John@Email.com",<br/>
> "phone": "(41)90000-0000"<br/>
> }

Modelo de resposta de sucesso, 201:

>{<br/>
>    "name": "John Doe dOe",<br/>
>    "email": "john@email.com",<br/>
>    "phone": "(41)90000-0000",<br/>
>    "creation_date": "Fri, 10 Sep 2021 17:53:25 GMT", <br/>
>    "last_visit": "Fri, 10 Sep 2021 17:53:25 GMT", <br/>
>    "visits": 1<br/>
>}

<br/>

## Possíveis erros - POST
#### Falta de chaves na requisição.
Retorno esperado, 400:

>{<br/>
>    "error": "Faltando a chave necessária: email<br/>
>}

#### Chaves desnecessárias na requisição.
Retorno esperado, 400:

>{<br/>
>"error": "Há chaves excessivas na requisição. As necessárias são: 'email', 'name', 'phone'."<br/>
>}


#### Formato irregular da string do telefone.
Retorno esperado, 400:

>{
>"error": "Verique o formato do valor 'phone'. Formato aceito é: (XX)XXXXX-XXXX."<br/>
>}

#### Email ou phone já existente no banco de dados.
Retorno esperado, 409:

>{<br/>
>"error": "email já existente"<br/>
>}
<br/>

## GET - lista todos os usuários

Não tem corpo na requisição.

Modelo de resposta de sucesso, 200:


>{<br/>
>"leads": [<br/>
>    {<br/>
>    "name": "John Doe",<br/>
>    "email": "john@email.com",<br/>
>    "phone": "(41)90000-0000",<br/>
>    "creation_date": "Sun, 06 Mar 2022 18:30:55 GMT",<br/>
>    "last_visit": "Sun, 06 Mar 2022 18:30:55 GMT",<br/>
>    "visits": 1<br/>
>    }<br/>
>]<br/>
>}

## Possível erro - GET
#### Lista vazia.
Retorno esperado, 404:
>{"error": "O banco de dados está vazio"}


## UPDATE - atualiza data de visita e número de visita.
Modelo de requisição:
>{<br/>
    "email": "john@email.com" <br/>
}

Em caso de sucesso não há retorno esperado, 204.

## Possíveis erros - UPDATE
#### Ausência da chave email.
Retorno esperado, 400:
>{"error": "Erro na chave email"}

#### Valor diferente de string no campo email
Retorno esperado, 400:
>{"error": "Informe um valor do email em formato 'string'."}

#### Email não cadastrado no banco de dados.
Retorno esperado, 404:
>{"error": "Lead não encontrado"}


## DELETE - apaga lead do banco de dados.
Modelo de requisição:
>{<br/>
    "email": "john@email.com" <br/>
}

Em caso de sucesso não há retorno esperado, 204.

## Possíveis erros - DELETE
#### Ausência da chave email.
Retorno esperado, 400:
>{"error": "Erro na chave email"}

#### Valor diferente de string no campo email
Retorno esperado, 400:
>{"error": "Informe um valor do email em formato 'string'."}

#### Email não cadastrado no banco de dados.
Retorno esperado, 404:
>{"error": "Lead não encontrado"}

