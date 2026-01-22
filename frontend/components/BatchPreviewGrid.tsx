"use client";

import { useEffect, useMemo } from "react";

type Props = {
  files: File[];
};

type Preview = {
  url: string;
  name: string;
};

export default function BatchPreviewGrid({ files }: Props) {
  const previews = useMemo<Preview[]>(() => {
    return files.map((file) => ({
      url: URL.createObjectURL(file),
      name: file.name,
    }));
  }, [files]);

  // Cleanup object URLs to avoid memory leaks
  useEffect(() => {
    return () => {
      previews.forEach((p) => URL.revokeObjectURL(p.url));
    };
  }, [previews]);

  if (!files || files.length === 0) {
    return (
      <div className="text-sm text-slate-400">
        No preview available. Upload images to see thumbnails.
      </div>
    );
  }

  return (
    <div className="grid grid-cols-3 sm:grid-cols-4 md:grid-cols-5 gap-3">
      {previews.map((p, idx) => (
        <div
          key={`${p.name}-${idx}`}
          className="relative aspect-square overflow-hidden rounded-xl border border-slate-800 bg-slate-900/40"
        >
          {/* eslint-disable-next-line @next/next/no-img-element */}
          <img
            src={p.url}
            alt={p.name}
            className="h-full w-full object-cover"
          />

          <div className="absolute bottom-0 left-0 right-0 bg-black/60 px-1 py-0.5 text-[10px] text-slate-200 truncate">
            {p.name}
          </div>
        </div>
      ))}
    </div>
  );
}
