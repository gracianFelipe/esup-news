import Link from "next/link";
import { THEMES } from "@/lib/mock/themes";

export function Footer() {
  return (
    <footer className="mt-32 border-t border-paper/10">
      <div className="mx-auto max-w-editorial px-6 py-16 md:px-10 md:py-24">
        <div className="grid gap-12 md:grid-cols-12">
          <div className="md:col-span-5">
            <div className="font-serif text-3xl tracking-tightest md:text-4xl">
              The <span className="text-accent">Prism</span>
            </div>
            <p className="mt-5 max-w-md text-[15px] leading-relaxed text-paper/70">
              Um jornal de curadoria, organizado por temas. Curadoria semanal, leitura sem ruído.
            </p>
          </div>

          <div className="md:col-span-4">
            <div className="eyebrow mb-4">temas</div>
            <ul className="space-y-2 text-[14px]">
              {THEMES.map((t) => (
                <li key={t.slug}>
                  <Link
                    href={`/tema/${t.slug}`}
                    className="editorial-link text-paper/85 hover:text-paper"
                  >
                    {t.name}
                  </Link>
                </li>
              ))}
            </ul>
          </div>

          <div className="md:col-span-3">
            <div className="eyebrow mb-4">edição</div>
            <p className="text-[13px] leading-relaxed text-paper/60">
              As notícias são coletadas automaticamente de fontes públicas e
              organizadas por tema. Cada matéria leva à publicação original.
            </p>
          </div>
        </div>

        <div className="mt-16 flex items-center justify-between border-t border-paper/10 pt-6">
          <span className="eyebrow">© the prism — 2026</span>
          <span className="eyebrow">prototype · v0.1</span>
        </div>
      </div>
    </footer>
  );
}
