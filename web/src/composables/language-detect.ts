import flourite from "flourite";
import { codeToHtml, createHighlighter } from "shiki";

export function useLanguageDetector(code: string){
    const language = flourite(code, { shiki: true, noUnknown: true });
    console.info(`Detected language: ${language.language}`)
    return language.language
}

const highlighter = await createHighlighter({
  themes: ["github-light"],
  langs: [
    "javascript",
    "typescript",
    "python",
    "go",
    "rust",
    "json",
    "bash",
    "julia",
    "kotlin",
    "html",
    "css",
    "markdown"
  ],
});

export async function useShikiHighlighter(code: string, language: string){
  return highlighter.codeToHtml(code, {
    lang: language,
    theme: 'github-light'
  })
}
