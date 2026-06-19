import { FormEvent, useState } from "react";

interface QueryPanelProps {
  busy: boolean;
  onAsk: (question: string, topK: number) => Promise<void>;
}

export function QueryPanel({ busy, onAsk }: QueryPanelProps) {
  const [question, setQuestion] = useState("");
  const [topK, setTopK] = useState(5);

  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed) {
      return;
    }
    await onAsk(trimmed, topK);
  }

  return (
    <section className="panel">
      <div className="panel-heading">
        <h2>Question Form</h2>
      </div>
      <form className="stack" onSubmit={submit}>
        <label>
          Question
          <textarea value={question} onChange={(event) => setQuestion(event.target.value)} rows={4} />
        </label>
        <label className="compact-label">
          Top K
          <input
            type="number"
            min={1}
            max={20}
            value={topK}
            onChange={(event) => setTopK(Number(event.target.value))}
          />
        </label>
        <button type="submit" disabled={busy || question.trim().length === 0}>
          {busy ? "Asking..." : "Ask"}
        </button>
      </form>
    </section>
  );
}
