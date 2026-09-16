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
    "html",
    "css",
    "scss",
    "python",
    "go",
    "rust",
    "java",
    "c",
    "cpp",
    "csharp",
    "bash",
    "shellsession",
    "powershell",
    "yaml",
    "toml",
    "json",
    "sql",
    "ruby",
    "php",
    "kotlin",
    "swift",
    "markdown",
  ],
});

export function useShikiHighlighter(code: string, language: string) {
  return highlighter.codeToHtml(code, {
    lang: language,
    theme: 'github-light'
  })
}
