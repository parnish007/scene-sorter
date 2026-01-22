export const ALLOWED_MIME_TYPES = new Set([
  "image/jpeg",
  "image/png",
  "image/webp"
]);

export const DEFAULT_MAX_FILES = 200;
export const DEFAULT_MAX_FILE_SIZE_MB = 10;

export type ValidationResult =
  | { ok: true }
  | { ok: false; error: string };

export function validateFiles(
  files: File[],
  maxFiles: number = DEFAULT_MAX_FILES,
  maxFileSizeMB: number = DEFAULT_MAX_FILE_SIZE_MB
): ValidationResult {
  if (!files || files.length === 0) {
    return { ok: false, error: "Please select at least one image." };
  }

  if (files.length > maxFiles) {
    return { ok: false, error: `Too many files. Max allowed is ${maxFiles}.` };
  }

  for (const file of files) {
    if (!ALLOWED_MIME_TYPES.has(file.type)) {
      return {
        ok: false,
        error: `Unsupported file type: ${file.name} (${file.type || "unknown"})`
      };
    }

    const sizeMB = file.size / (1024 * 1024);
    if (sizeMB > maxFileSizeMB) {
      return {
        ok: false,
        error: `File too large: ${file.name} (${sizeMB.toFixed(
          2
        )} MB). Max is ${maxFileSizeMB} MB.`
      };
    }
  }

  return { ok: true };
}
