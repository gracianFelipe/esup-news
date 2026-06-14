"""Exporta os artigos classificados para o portal Prisma (snapshot JSON).

Gera `web/lib/data/articles.json` espelhando o tipo `Article` do portal
(`web/lib/types.ts`). Cada artigo é atribuído ao seu tema de maior score
(o portal usa o modelo de 1 tema por artigo). Só entram matches com
`relevance_score >= cutoff`. O artigo de maior score de cada tema vira `featured`.

Re-rode após cada `ingest` para atualizar o portal:
    python -m esup_news.cli export-web
"""
from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
from pathlib import Path

from ..config import PROJECT_ROOT, settings

DEFAULT_OUT = PROJECT_ROOT / "web" / "lib" / "data" / "articles.json"

# stopwords curtas só para gerar slugs limpos (kebab-case, sem acento)
_SLUG_STOP = {
    "a", "o", "as", "os", "um", "uma", "de", "da", "do", "das", "dos", "e", "ou",
    "em", "no", "na", "nos", "nas", "para", "por", "com", "sem", "que", "se",
    "ao", "aos", "the", "of", "in", "on", "to", "for", "and", "or", "with",
}


def _slugify(title: str) -> str:
    t = unicodedata.normalize("NFKD", title.lower()).encode("ascii", "ignore").decode("ascii")
    words = re.sub(r"[^a-z0-9]+", " ", t).split()
    parts = [w for w in words if w not in _SLUG_STOP and len(w) > 1]
    slug = "-".join(parts or words)
    return slug[:80].strip("-") or "materia"


# NewsData/The News API no plano grátis cortam o conteúdo com este marcador.
_PAYWALL = re.compile(r"only available in paid plans?.*$", re.IGNORECASE | re.DOTALL)


def _clean(text: str | None) -> str:
    if not text:
        return ""
    t = _PAYWALL.sub("", text).replace(" ", " ")
    t = re.sub(r"[ \t]+", " ", t)
    t = re.sub(r"\n{3,}", "\n\n", t).strip()
    return t


def _summary(text: str, limit: int = 240) -> str:
    """Resumo curto: até ~limit chars, cortado em fim de frase quando der."""
    if len(text) <= limit:
        return text
    cut = text[:limit]
    end = max(cut.rfind(". "), cut.rfind("! "), cut.rfind("? "))
    if end >= 100:
        return cut[: end + 1].strip()
    sp = cut.rfind(" ")
    return (cut[:sp] if sp > 0 else cut).strip() + "…"


def export_web(
    conn: sqlite3.Connection,
    out_path: Path | None = None,
    *,
    cutoff: int | None = None,
) -> tuple[int, Path]:
    out = Path(out_path) if out_path else DEFAULT_OUT
    cut = settings.score_cutoff if cutoff is None else cutoff

    rows = conn.execute(
        """
        WITH ranked AS (
          SELECT m.article_id, m.course_id, m.relevance_score,
                 ROW_NUMBER() OVER (
                   PARTITION BY m.article_id
                   ORDER BY m.relevance_score DESC, m.course_id ASC
                 ) AS rn
          FROM article_course_matches m
          WHERE m.relevance_score >= ?
        )
        SELECT a.id, a.title, a.description, a.snippet, a.url,
               a.source_name, a.source_domain, a.published_at,
               co.slug AS theme_slug, r.relevance_score AS score
        FROM ranked r
        JOIN articles a ON a.id = r.article_id
        JOIN courses co ON co.id = r.course_id
        WHERE r.rn = 1
        ORDER BY a.published_at DESC
        """,
        (cut,),
    ).fetchall()

    # maior score por tema -> featured
    top_by_theme: dict[str, tuple[int, int]] = {}
    for r in rows:
        best = top_by_theme.get(r["theme_slug"])
        if best is None or r["score"] > best[0]:
            top_by_theme[r["theme_slug"]] = (r["score"], r["id"])
    featured_ids = {aid for _, aid in top_by_theme.values()}

    seen: set[str] = set()
    articles: list[dict] = []
    for r in rows:
        base = _slugify(r["title"])
        slug = base if base not in seen else f"{base}-{r['id']}"
        seen.add(slug)

        desc = _clean(r["description"])
        snip = _clean(r["snippet"])
        full = desc if len(desc) >= len(snip) else snip  # o mais completo dos dois
        subtitle = _summary(full)                        # resumo curto p/ cards
        body = full                                      # conteúdo completo p/ a página
        source = (r["source_name"] or r["source_domain"] or "fonte").strip()

        articles.append(
            {
                "id": f"a{r['id']}",
                "slug": slug,
                "themeSlug": r["theme_slug"],
                "title": (r["title"] or "").strip(),
                "subtitle": subtitle,
                "body": body,
                "source": source,
                "publishedAt": r["published_at"],
                "externalUrl": r["url"],
                "featured": r["id"] in featured_ids,
                "imageSeed": f"a{r['id']}",
            }
        )

    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(articles, ensure_ascii=False, indent=2), encoding="utf-8")
    return len(articles), out
