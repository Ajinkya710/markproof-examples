# Markproof examples

Working examples for [Markproof](https://markproof.co): an invisible watermark plus signed C2PA Content Credentials on AI-generated images and audio, in one API call, for the EU AI Act's Article 50.

> **Is your AI output Article 50-ready?** Drop a file into the [free checker](https://markproof.co/check). No signup needed.

| Example | What it shows |
|---|---|
| [`nextjs/`](nextjs) | Next.js App Router: mark images server-side with the `markproof` npm package; signed batch webhook receiver |
| [`fastapi/`](fastapi) | FastAPI: mark images with the `markproof` PyPI package; signed batch webhook receiver; offline tests |
| [`claude-agent/`](claude-agent) | A Claude agent (Anthropic Python SDK) marking and verifying its images through the `markproof-mcp` server |
| [`comfyui/`](comfyui) | ComfyUI workflow using the Markproof: Mark & Save node |

Every example needs a Markproof API key: 250 free calls a month at [markproof.co/dashboard](https://markproof.co/dashboard). API reference: [markproof.co/docs](https://markproof.co/docs).

MIT licensed.
