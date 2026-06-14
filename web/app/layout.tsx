import type { Metadata } from "next";
import "./globals.css";
import { Header } from "@/components/Header";
import { Footer } from "@/components/Footer";
import { ThemeScript } from "@/components/ThemeScript";
import { ScrollProgress } from "@/components/ScrollProgress";
import { CursorHalo } from "@/components/CursorHalo";
import { ThemeTracker } from "@/components/ThemeTracker";

export const metadata: Metadata = {
  title: "The Prism — Jornal de curadoria",
  description:
    "As notícias mais atuais, organizadas por tema, em um só lugar. Justiça, Negócios, Tecnologia, Gestão, Educação, Finanças e Comportamento.",
  applicationName: "The Prism",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="pt-BR" suppressHydrationWarning>
      <head>
        <ThemeScript />
      </head>
      <body className="relative min-h-screen overflow-x-hidden bg-ink text-paper antialiased">
        <CursorHalo />
        <ScrollProgress />
        <Header />
        <main className="relative z-10">{children}</main>
        <ThemeTracker />
        <Footer />
      </body>
    </html>
  );
}
