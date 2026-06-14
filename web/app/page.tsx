import { Hero } from "@/components/Hero";
import { LatestStrip } from "@/components/LatestStrip";
import { ThemesIndex } from "@/components/ThemesIndex";
import { ThemeBlock } from "@/components/ThemeBlock";
import { Closing } from "@/components/Closing";
import { THEMES } from "@/lib/mock/themes";

export default function HomePage() {
  return (
    <>
      <Hero />
      <LatestStrip />
      <ThemesIndex />
      {THEMES.map((theme, i) => (
        <ThemeBlock key={theme.slug} theme={theme} index={i} />
      ))}
      <Closing />
    </>
  );
}
