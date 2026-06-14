import Link from "next/link";
import type { Article } from "@/lib/types";
import { AbstractCover } from "./AbstractCover";
import { formatRelative } from "@/lib/format";
import { getTheme } from "@/lib/mock/themes";

type Size = "hero" | "feature" | "regular" | "compact" | "list";

type Props = {
  article: Article;
  size?: Size;
  showTheme?: boolean;
};

export function NewsCard({ article, size = "regular", showTheme = false }: Props) {
  const theme = getTheme(article.themeSlug);
  const href = `/noticia/${article.slug}`;

  if (size === "list") {
    return (
      <Link href={href} className="group block border-t border-paper/10 py-7">
        <div className="grid grid-cols-12 gap-6">
          <div className="col-span-12 md:col-span-9">
            {showTheme && theme && (
              <div className="eyebrow mb-3">{theme.label}</div>
            )}
            <h3 className="font-serif text-2xl leading-[1.18] tracking-tight text-paper transition-colors group-hover:text-accent md:text-3xl md:leading-[1.15] md:tracking-tightest">
              {article.title}
            </h3>
            <p className="mt-3 max-w-2xl text-[15px] leading-relaxed text-paper/70">
              {article.subtitle}
            </p>
          </div>
          <div className="col-span-12 flex items-start justify-between gap-4 text-paper/55 md:col-span-3 md:flex-col md:items-end md:gap-2">
            <span className="eyebrow">{article.source}</span>
            <span className="eyebrow">{formatRelative(article.publishedAt)}</span>
          </div>
        </div>
      </Link>
    );
  }

  const ratio =
    size === "hero" ? "wide" : size === "feature" ? "wide" : size === "compact" ? "square" : "wide";

  const titleClasses =
    size === "hero"
      ? "font-serif text-4xl leading-[1.12] tracking-tight md:text-6xl md:leading-[1.05] md:tracking-tightest"
      : size === "feature"
        ? "font-serif text-3xl leading-[1.15] tracking-tight md:text-4xl md:leading-[1.08] md:tracking-tightest"
        : size === "compact"
          ? "font-serif text-xl leading-[1.15] tracking-tight md:text-2xl md:tracking-tightest"
          : "font-serif text-2xl leading-[1.18] tracking-tight md:text-[1.7rem] md:leading-[1.1] md:tracking-tightest";

  const subtitleClasses =
    size === "compact"
      ? "mt-2 text-[13px] leading-relaxed text-paper/65 line-clamp-2"
      : "mt-3 text-[15px] leading-relaxed text-paper/70 line-clamp-3";

  return (
    <Link href={href} className="group block">
      <div className="overflow-hidden">
        <div className="hover-zoom">
          <AbstractCover seed={article.imageSeed} ratio={ratio} />
        </div>
      </div>
      <div className="mt-5 flex items-center justify-between">
        <div className="flex items-center gap-3">
          {showTheme && theme && <span className="eyebrow">{theme.label}</span>}
        </div>
        <span className="eyebrow">{formatRelative(article.publishedAt)}</span>
      </div>
      <h3 className={`mt-2 ${titleClasses} text-paper transition-colors group-hover:text-accent`}>
        {article.title}
      </h3>
      <p className={subtitleClasses}>{article.subtitle}</p>
      <div className="mt-4 flex items-center gap-3 text-paper/55">
        <span className="eyebrow">{article.source}</span>
      </div>
    </Link>
  );
}
