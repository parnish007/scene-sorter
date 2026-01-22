import { Camera, FolderDown, Sparkles } from "lucide-react";

export default function Navbar() {
  return (
    <nav className="border-b border-slate-800 bg-slate-950/60 backdrop-blur">
      <div className="container py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="h-10 w-10 rounded-2xl bg-white text-slate-950 flex items-center justify-center">
            <Sparkles size={18} />
          </div>
          <div>
            <div className="font-semibold leading-tight">Scene Sorter</div>
            <div className="text-xs text-slate-400">
              Batch classify & auto-organize photos
              made by @trilochan_sharma aka parnish
            </div>
          </div>
        </div>

        <div className="flex items-center gap-3 text-slate-300">
          <div className="hidden md:flex items-center gap-2 text-sm">
            <Camera size={16} />
            Upload / Capture
          </div>
          <div className="hidden md:flex items-center gap-2 text-sm">
            <FolderDown size={16} />
            Download ZIP
          </div>
        </div>
      </div>
    </nav>
  );
}
