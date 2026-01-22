type Props = {
  progress: number; // 0–100
};

export default function UploadProgress({ progress }: Props) {
  return (
    <div className="space-y-2">
      <div className="text-sm text-slate-300">
        Uploading & processing images…
      </div>

      <div className="h-2 w-full overflow-hidden rounded-full bg-slate-800">
        <div
          className="h-full rounded-full bg-white transition-all"
          style={{ width: `${Math.min(Math.max(progress, 0), 100)}%` }}
        />
      </div>

      <div className="text-xs text-slate-500">{progress}%</div>
    </div>
  );
}
