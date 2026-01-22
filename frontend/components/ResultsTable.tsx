import type { ImagePrediction } from "@/lib/api";

type Props = {
  results: ImagePrediction[];
  summary: {
    total: number;
    by_class: Record<string, number>;
  };
};

function formatPercent(x: number): string {
  const pct = x * 100;
  return `${pct.toFixed(2)}%`;
}

export default function ResultsTable({ results, summary }: Props) {
  const byClassEntries = Object.entries(summary.by_class || {}).sort(
    (a, b) => b[1] - a[1]
  );

  return (
    <div className="space-y-6">
      {/* Summary */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        <div className="rounded-2xl border border-slate-800 bg-slate-950/30 p-4">
          <div className="text-sm text-slate-400">Total Images</div>
          <div className="text-2xl font-semibold mt-1">{summary.total}</div>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-950/30 p-4">
          <div className="text-sm text-slate-400">By Class</div>
          <div className="mt-2 flex flex-wrap gap-2">
            {byClassEntries.length === 0 && (
              <div className="text-sm text-slate-300">No summary available.</div>
            )}

            {byClassEntries.map(([label, count]) => (
              <span
                key={label}
                className="rounded-xl border border-slate-700 bg-slate-900/40 px-3 py-1 text-sm"
              >
                <span className="text-slate-200 font-medium">{label}</span>
                <span className="text-slate-400"> · {count}</span>
              </span>
            ))}
          </div>
        </div>
      </div>

      {/* Table */}
      <div className="overflow-hidden rounded-2xl border border-slate-800">
        <table className="w-full text-sm">
          <thead className="bg-slate-900/60">
            <tr>
              <th className="text-left px-4 py-3 font-medium text-slate-200">
                Filename
              </th>
              <th className="text-left px-4 py-3 font-medium text-slate-200">
                Prediction
              </th>
              <th className="text-left px-4 py-3 font-medium text-slate-200">
                Confidence
              </th>
            </tr>
          </thead>

          <tbody className="bg-slate-950/40">
            {results.map((r, idx) => (
              <tr
                key={`${r.filename}-${idx}`}
                className="border-t border-slate-800"
              >
                <td className="px-4 py-3 text-slate-200 break-all">
                  {r.filename}
                </td>
                <td className="px-4 py-3">
                  <span className="inline-flex items-center rounded-xl border border-slate-700 bg-slate-900/40 px-3 py-1">
                    {r.label}
                  </span>
                </td>
                <td className="px-4 py-3 text-slate-300">
                  {formatPercent(r.confidence)}
                </td>
              </tr>
            ))}

            {results.length === 0 && (
              <tr className="border-t border-slate-800">
                <td className="px-4 py-6 text-slate-400" colSpan={3}>
                  No results to display.
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
