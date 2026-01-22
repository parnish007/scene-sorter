"use client";

import { useMemo, useState } from "react";
import Navbar from "@/components/Navbar";
import UploadDropzone from "@/components/UploadDropzone";
import BatchPreviewGrid from "@/components/BatchPreviewGrid";
import UploadProgress from "@/components/UploadProgress";
import ResultsTable from "@/components/ResultsTable";
import DownloadZipCard from "@/components/DownloadZipCard";

import { batchPredict, BatchPredictResponse } from "@/lib/api";
import { validateFiles } from "@/lib/validators";

type UiState =
  | { status: "idle" }
  | { status: "uploading"; progress: number }
  | { status: "done"; data: BatchPredictResponse; downloadUrl: string }
  | { status: "error"; message: string };

export default function HomePage() {
  const [selectedFiles, setSelectedFiles] = useState<File[]>([]);
  const [ui, setUi] = useState<UiState>({ status: "idle" });

  const canSubmit = useMemo(() => selectedFiles.length > 0 && ui.status !== "uploading", [
    selectedFiles.length,
    ui.status,
  ]);

  async function onRunBatch() {
    const check = validateFiles(selectedFiles);
    if (!check.ok) {
      setUi({ status: "error", message: check.error });
      return;
    }

    // We can't truly measure server-side progress with plain fetch,
    // but we can show a simple "fake" progress indicator for UX.
    setUi({ status: "uploading", progress: 10 });

    const tick = window.setInterval(() => {
      setUi((prev) => {
        if (prev.status !== "uploading") return prev;
        const next = Math.min(prev.progress + 8, 90);
        return { status: "uploading", progress: next };
      });
    }, 250);

    try {
      const { data, downloadUrl } = await batchPredict(selectedFiles);
      window.clearInterval(tick);
      setUi({ status: "done", data, downloadUrl });
    } catch (err: any) {
      window.clearInterval(tick);
      setUi({
        status: "error",
        message: err?.message || "Something went wrong while uploading.",
      });
    }
  }

  function onClear() {
    setSelectedFiles([]);
    setUi({ status: "idle" });
  }

  return (
    <>
      <Navbar />

      <main className="container py-10">
        <div className="space-y-8">
          <header className="space-y-3">
            <h1 className="text-3xl md:text-4xl font-semibold">
              Scene Sorter — AI Photo Organizer
            </h1>
            <p className="text-slate-300 max-w-3xl">
              Upload a batch of travel photos (10–100). The backend predicts the scene
              (buildings, forest, glacier, mountain, sea, street), organizes them into
              folders, and gives you a ZIP to download.
            </p>
          </header>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <section className="rounded-2xl border border-slate-800 bg-slate-900/30 p-5">
              <h2 className="text-lg font-medium mb-3">Upload Photos</h2>

              <UploadDropzone
                files={selectedFiles}
                onFilesChange={setSelectedFiles}
              />

              <div className="mt-4 flex flex-wrap gap-3">
                <button
                  className="px-4 py-2 rounded-xl bg-white text-slate-950 font-medium disabled:opacity-50"
                  onClick={onRunBatch}
                  disabled={!canSubmit}
                >
                  Run Batch Classification
                </button>

                <button
                  className="px-4 py-2 rounded-xl border border-slate-700 text-slate-100 disabled:opacity-50"
                  onClick={onClear}
                  disabled={ui.status === "uploading"}
                >
                  Clear
                </button>
              </div>

              {ui.status === "error" && (
                <div className="mt-4 rounded-xl border border-red-900/60 bg-red-950/40 p-3 text-red-200">
                  {ui.message}
                </div>
              )}

              {ui.status === "uploading" && (
                <div className="mt-4">
                  <UploadProgress progress={ui.progress} />
                </div>
              )}
            </section>

            <section className="rounded-2xl border border-slate-800 bg-slate-900/30 p-5">
              <h2 className="text-lg font-medium mb-3">Preview</h2>
              <BatchPreviewGrid files={selectedFiles} />
            </section>
          </div>

          {ui.status === "done" && (
            <section className="rounded-2xl border border-slate-800 bg-slate-900/30 p-5 space-y-6">
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div>
                  <h2 className="text-xl font-semibold">Results</h2>
                  <p className="text-slate-300">
                    Total images: <span className="text-slate-100 font-medium">{ui.data.summary.total}</span>
                  </p>
                </div>

                <DownloadZipCard
                  downloadUrl={ui.downloadUrl}
                  jobId={ui.data.job_id}
                />
              </div>

              <ResultsTable results={ui.data.results} summary={ui.data.summary} />
            </section>
          )}
        </div>
      </main>

      <footer className="container py-8 text-slate-400 text-sm">
        Built with Next.js + FastAPI + TensorFlow. Designed for batch upload → folder sorting → ZIP download.
      </footer>
    </>
  );
}
