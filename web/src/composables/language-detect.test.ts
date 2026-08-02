import { describe, expect, test } from 'vitest'
import { useLanguageDetector } from './language-detect'



const html_snippet = `<!DOCTYPE html>
<html>
<head>
<title>Page Title</title>
</head>
<body>

<h1>This is a Heading</h1>
<p>This is a paragraph.</p>

</body>
</html>`

const go_snippet = `package main

import "fmt"

func main() {
    fmt.Println("hello world")
}`

const python_snippet = `import time

start_time = time.time()

# printing all even numbers till 20
for i in range(20):
  if i % 2 == 0:
    print(i, end = " ")

end_time = time.time()
time_taken = end_time - start_time
print("Time: ", time_taken)`


const cases = [
	{ language: "python", code: python_snippet },
	{ language: "go", code: go_snippet },
	{ language: "html", code: html_snippet },
]


describe("Test the useLanguageDetector compsable sanity", () => {
	test.each(cases)(
		"detects $language",
		({ language, code }) => {
			expect(useLanguageDetector(code)).toBe(language)
		}
	)
})

