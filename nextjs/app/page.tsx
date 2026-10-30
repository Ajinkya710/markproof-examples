"use client";

import { useState, type FormEvent } from "react";

export default function Page() {
  const [result, setResult] = useState<{ url: string; verifyUrl: string; code: string } | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);

  async function onSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault();
    setBusy(true);
    setError(null);
    const response = await fetch("/api/mark", { method: "POST", body: new FormData(e.currentTarget) });
    setBusy(false);
    if (!response.ok) {
      setError((await response.json()).error);
      return;
    }
    setResult({
      url: URL.createObjectURL(await response.blob()),
      verifyUrl: response.headers.get("x-verify-url")!,
      code: response.headers.get("x-watermark-code")!,
    });
  }

  return (
    <main>
      <h1>Mark an AI-generated image</h1>
      <form onSubmit={onSubmit}>
        <input type="file" name="file" accept="image/png,image/jpeg,image/webp" required />
        <label style={{ display: "block", margin: "12px 0" }}>
          <input type="checkbox" name="label" /> Add a visible &ldquo;AI-generated&rdquo; label
        </label>
        <button disabled={busy}>{busy ? "Marking…" : "Mark it"}</button>
      </form>
      {error && <p style={{ color: "crimson" }}>{error}</p>}
      {result && (
        <section>
          <img src={result.url} alt="Marked result" style={{ maxWidth: "100%", marginTop: 24 }} />
          <p>
            Watermark code <code>{result.code}</code>.{" "}
            <a href={result.verifyUrl}>Public verify page</a> ·{" "}
            <a href={result.url} download="marked.png">Download</a> (then drop it into{" "}
            <a href="https://markproof.co/check">the free checker</a>)
          </p>
        </section>
      )}
    </main>
  );
}
