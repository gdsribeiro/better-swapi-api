# Better SWAPI

**Better SWAPI** é uma API wrapper robusta e aprimorada para a [Star Wars API (SWAPI)](https://swapi.dev/), construída com Python.

Este projeto adiciona funcionalidades a API original, oferecendo recursos como:
- **Filtragem**: múltiplos campos.
- **Ordenação**: `sort_by` e `order`.
- **Paginação**: `page` e `limit`.
- **Seleção**: `fields`.

## 🔐 Autenticação

Esta API é protegida via **API Key**. Para realizar requisições, você deve incluir o cabeçalho `x-api-key` com sua chave de acesso válida disponibilizada pelo administrador (@gdsribeiro).

## 🚀 Endpoints

A API expõe os seguintes recursos principais. Todos os endpoints suportam o método `GET`.

### 🎬 Filmes (`/filmes`)
Retorna a lista de filmes da saga Star Wars.

**Filtros Específicos:**
- `title`
- `episode_id`
- `opening_crawl`
- `director`
- `producer`
- `release_date`

**Exemplo:**
```bash
curl -X GET "https://<url>/filmes?title=Hope&sort_by=release_date&order=asc" \
     -H "x-api-key: SUA_CHAVE_AQUI"
```

### 🦸 Personagens (`/personagens`)
Retorna a lista de personagens.

**Filtros Específicos:**
- `name`
- `birth_year`
- `eye_color`
- `gender`
- `hair_color`
- `height`
- `mass`
- `skin_color`

**Exemplo:**
```bash
curl -X GET "https://<url>/personagens?name=Luke&fields=name,homeworld" \
     -H "x-api-key: SUA_CHAVE_AQUI"
```

### 🪐 Planetas (`/planetas`)
Retorna a lista de planetas.

**Filtros Específicos:**
- `name`
- `rotation_period`
- `orbital_period`
- `diameter`
- `climate`
- `gravity`
- `terrain`
- `surface_water`
- `population`

**Exemplo:**
```bash
curl -X GET "https://<url>/planetas?page=2&limit=5" \
     -H "x-api-key: SUA_CHAVE_AQUI"
```

### 🚀 Naves (`/naves`)
Retorna a lista de naves estelares.

**Filtros Específicos:**
- `name`
- `model`
- `manufacturer`
- `cost_in_credits`
- `length`
- `max_atmosphering_speed`
- `crew`
- `passengers`
- `cargo_capacity`
- `consumables`
- `hyperdrive_rating`
- `MGLT`
- `starship_class`

**Exemplo:**
```bash
curl -X GET "https://<url>/naves?name=Falcon" \
     -H "x-api-key: SUA_CHAVE_AQUI"
```

---

## 🎛️ Parâmetros Globais

Estes parâmetros podem ser usados em **todos** os endpoints para refinar sua busca:

| Parâmetro | Descrição | Padrão | Exemplo |
| :--- | :--- | :--- | :--- |
| `page` | Número da página para paginação. | `1` | `?page=2` |
| `limit` | Quantidade de itens por página. | `10` | `?limit=20` |
| `sort_by` | Campo utilizado para ordenar os resultados. | Variável | `?sort_by=name` |
| `order` | Direção da ordenação (`asc` ou `desc`). | `asc` | `?order=desc` |
| `fields` | Lista de campos separados por vírgula para retornar. | Todos | `?fields=name,height` |

---

## 🛠️ Execução Local

Para rodar o projeto em sua máquina local para desenvolvimento ou testes:

### Pré-requisitos
- Python 3.8+
- Pip

### Passos

1. **Clone este repositório:**

2. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Execute a aplicação localmente:**
   Utilize o servidor de desenvolvimento do Flask:
   ```bash
   flask --app main run --port 8080 --debug
   ```
   A API estará disponível em `http://localhost:8080`.

---

## 🧪 Testes

O projeto possui uma suíte de testes unitários abrangente utilizando `pytest`.

Para executar os testes:

```bash
python -m pytest
```