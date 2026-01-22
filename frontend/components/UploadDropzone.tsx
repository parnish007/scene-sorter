"use client";

import { useCallback, useMemo } from "react";
import { useDropzone } from "react-dropzone";
import { ImagePlus, Trash2 } from "lucide-react";

import { ALLOWED_MIME_TYPES, validateFiles } from "@/lib/validators";

type Props = {
  files: File[];
  onFilesChange: (files: File[]) => void;
};

export default function UploadDropzone({ files, onFilesChange }: Props) {
  const accept = useMemo(() => {
    // react-dropzone expects: { 'image/*': [] } OR explicit mime mapping
    // We'll keep explicit for predictability.
    return {
      "image/jpeg": [],
      "image/png": [],
      "image/webp": [],
    };
  }, []);

  const onDrop = useCallback(
    (acceptedFiles: File[]) => {
      if (!acceptedFiles || acceptedFiles.length === 0) return;

      // Merge with existing
      const merged = [...files, ...acceptedFiles];

      // quick validation (same rules as page uses)
      const check = validateFiles(merged);
      if (!check.ok) {
        // If validation fails, keep old files (do not add)
        return;
      }

      onFilesChange(merged);
    },
    [files, onFilesChange]
  );

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept,
    multiple: true,
  });

  function removeFile(index: number) {
    const next = files.filter((_, i) => i !== index);
    onFilesChange(next);
  }

  const fileCountText =
    files.length === 0 ? "No files selected" : `${files.length} file(s) selected`;

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={[
          "rounded-2xl border border-dashed p-6 cursor-pointer transition",
          "bg-slate-950/30 border-slate-700 hover:border-slate-500",
          isDragActive ? "border-white/70 bg-slate-950/60" : "",
        ].join(" ")}
      >
        <input {...getInputProps()} />

        <div className="flex items-start gap-4">
          <div className="h-11 w-11 rounded-2xl bg-white/10 flex items-center justify-center">
            <ImagePlus size={18} />
          </div>

          <div className="space-y-1">
            <div className="font-medium">
              {isDragActive ? "Drop images here" : "Drag & drop images here"}
            </div>

            <div className="text-sm text-slate-400">
              Or click to browse. Supported: JPG, PNG, WEBP
            </div>

            <div className="text-xs text-slate-500">
              Tip: You can upload 10–100 photos and download an organized ZIP.
            </div>
          </div>
        </div>

        <div className="mt-4 text-sm text-slate-300">{fileCountText}</div>
      </div>

      {files.length > 0 && (
        <div className="rounded-2xl border border-slate-800 bg-slate-950/30 p-4">
          <div className="text-sm text-slate-300 mb-3">Selected files</div>

          <ul className="space-y-2 max-h-56 overflow-auto pr-1">
            {files.map((f, idx) => (
              <li
                key={`${f.name}-${idx}`}
                className="flex items-center justify-between gap-3 rounded-xl border border-slate-800 bg-slate-900/30 px-3 py-2"
              >
                <div className="min-w-0">
                  <div className="text-sm truncate">{f.name}</div>
                  <div className="text-xs text-slate-500">
                    {(f.size / (1024 * 1024)).toFixed(2)} MB • {f.type || "unknown"}
                  </div>
                </div>

                <button
                  type="button"
                  onClick={() => removeFile(idx)}
                  className="shrink-0 rounded-lg border border-slate-700 px-2 py-1 text-slate-200 hover:bg-slate-800"
                  title="Remove"
                >
                  <Trash2 size={16} />
                </button>
              </li>
            ))}
          </ul>

          <div className="mt-3 text-xs text-slate-500">
            Allowed types:{" "}
            <span className="text-slate-400">
              {Array.from(ALLOWED_MIME_TYPES).join(", ")}
            </span>
          </div>
        </div>
      )}
    </div>
  );
}
