"use client";

import { Download, CheckCircle2 } from "lucide-react";

type Props = {
  downloadUrl: string;
  jobId: string;
};

export default function DownloadZipCard({ downloadUrl, jobId }: Props) {
  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-950/30 p-4 flex flex-col sm:flex-row gap-3 sm:items-center sm:justify-between">
      <div className="flex items-start gap-3">
        <div className="h-10 w-10 rounded-2xl bg-white/10 flex items-center justify-center">
          <CheckCircle2 size={18} />
        </div>

        <div>
          <div className="font-medium">ZIP ready for download</div>
          <div className="text-xs text-slate-400">
            Job ID: <span className="text-slate-200">{jobId}</span>
          </div>
        </div>
      </div>

      <a
        href={downloadUrl}
        className="inline-flex items-center justify-center gap-2 px-4 py-2 rounded-xl bg-white text-slate-950 font-medium hover:opacity-90"
      >
        <Download size={18} />
        Download ZIP
      </a>
    </div>
  );
}
