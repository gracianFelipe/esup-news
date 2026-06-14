"""Constrói as queries de busca a partir das keywords de um curso.

Estratégia: separar keywords ativas em lotes e juntar com o operador OR.
A forma canônica usa " OR " (aceito direto pela NewsData.io). O The News API
não aceita "OR" literal — usa o pipe "|" —, então o TheNewsApiProvider
traduz " OR " para " | " ao chamar a API.

A NewsData.io tem um limite documentado de ~100 caracteres no parâmetro `q`.
Para respeitar esse limite, montamos as queries de forma incremental: enquanto
couber, agrupamos termos; quando estourar, fecha o lote e começa outro.
"""
from __future__ import annotations

import sqlite3

# Limite seguro de caracteres por query. NewsData rejeita acima de 100;
# deixamos margem para o quoting e o " OR ".
MAX_QUERY_LENGTH = 95

# Teto de termos por lote como salvaguarda — evita queries muito amplas que
# reduzem precisão.
MAX_TERMS_PER_QUERY = 6


def _quote(term: str) -> str:
    return f'"{term}"' if " " in term else term


def build_queries_for_course(conn: sqlite3.Connection, course_id: int) -> list[str]:
    rows = conn.execute(
        "SELECT term FROM keywords WHERE course_id = ? AND type = 'include' AND active = 1 "
        "ORDER BY weight DESC, id ASC",
        (course_id,),
    ).fetchall()
    terms = [r["term"] for r in rows]
    if not terms:
        return []

    queries: list[str] = []
    current: list[str] = []
    current_len = 0
    sep = " OR "

    for term in terms:
        quoted = _quote(term)
        # Se o termo sozinho já estoura, ele vira sua própria query (sem outros).
        if len(quoted) >= MAX_QUERY_LENGTH:
            if current:
                queries.append(sep.join(current))
                current, current_len = [], 0
            queries.append(quoted)
            continue

        # Comprimento se adicionarmos: separador + termo
        added = (len(sep) if current else 0) + len(quoted)
        would_be = current_len + added

        if (
            would_be > MAX_QUERY_LENGTH
            or len(current) >= MAX_TERMS_PER_QUERY
        ):
            queries.append(sep.join(current))
            current = [quoted]
            current_len = len(quoted)
        else:
            current.append(quoted)
            current_len = would_be

    if current:
        queries.append(sep.join(current))

    return queries
