import React, { useRef, useState } from 'react';
import { UploadCloud, FileText, Image, X, CheckCircle, AlertCircle } from 'lucide-react';

interface EvidenceUploadProps {
  selectedFile: File | null;
  onFileSelect: (file: File | null) => void;
  disabled?: boolean;
}

const ALLOWED_EXTENSIONS = ['.pdf', '.png', '.jpg', '.jpeg', '.webp'];
const MAX_SIZE_BYTES = 25 * 1024 * 1024; // 25 MB matches backend MAX_UPLOAD_SIZE_MB

export const EvidenceUpload: React.FC<EvidenceUploadProps> = ({
  selectedFile,
  onFileSelect,
  disabled = false,
}) => {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);
  const [uploadError, setUploadError] = useState<string | null>(null);

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  const validateAndSetFile = (file: File) => {
    setUploadError(null);

    // Validate size
    if (file.size > MAX_SIZE_BYTES) {
      setUploadError(`File exceeds maximum permitted size of 25 MB (${formatFileSize(file.size)}).`);
      return;
    }

    // Validate extension
    const ext = '.' + file.name.split('.').pop()?.toLowerCase();
    if (!ALLOWED_EXTENSIONS.includes(ext)) {
      setUploadError(
        `Unsupported file type (${ext}). Only PDF documents and PNG/JPEG/WEBP images are permitted.`
      );
      return;
    }

    onFileSelect(file);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (disabled) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndSetFile(e.dataTransfer.files[0]);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!disabled) setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleFileInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndSetFile(e.target.files[0]);
    }
  };

  const getFileIcon = (filename: string) => {
    const ext = filename.split('.').pop()?.toLowerCase();
    if (ext === 'pdf') {
      return <FileText className="w-6 h-6 text-rose-400" />;
    }
    return <Image className="w-6 h-6 text-cyan-400" />;
  };

  return (
    <div className="mt-4">
      <div className="flex items-center justify-between mb-1.5">
        <label className="text-xs font-mono font-semibold text-slate-300 uppercase tracking-wider flex items-center space-x-1.5">
          <span>Digital Artifact / Document Upload</span>
          <span className="text-[10px] text-slate-500 font-normal lowercase">(optional)</span>
        </label>
        <span className="text-[10px] text-slate-400 font-mono">
          PDF, PNG, JPG (Max 25 MB)
        </span>
      </div>

      <input
        type="file"
        ref={fileInputRef}
        onChange={handleFileInputChange}
        accept=".pdf,.png,.jpg,.jpeg,.webp"
        className="hidden"
        disabled={disabled}
      />

      {/* Upload Box or Selected File Card */}
      {!selectedFile ? (
        <div
          onDrop={handleDrop}
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onClick={() => !disabled && fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-lg p-4 text-center cursor-pointer transition-all duration-200 ${
            isDragging
              ? 'border-cyan-400 bg-cyan-950/20'
              : 'border-slate-800 hover:border-slate-700 bg-slate-900/40 hover:bg-slate-900/70'
          } ${disabled ? 'opacity-50 cursor-not-allowed' : ''}`}
        >
          <div className="flex flex-col items-center justify-center space-y-2">
            <div className="p-2.5 rounded-full bg-slate-800/80 border border-slate-700/60 text-slate-400">
              <UploadCloud className="w-5 h-5 text-cyan-400" />
            </div>
            <div>
              <p className="text-xs text-slate-300 font-medium">
                Drag and drop suspicious court notice, warrant, or bank screenshot
              </p>
              <p className="text-[11px] text-slate-500 mt-0.5">
                or <span className="text-cyan-400 underline underline-offset-2">browse local file</span> for magic-byte signature verification
              </p>
            </div>
          </div>
        </div>
      ) : (
        <div className="p-3 rounded-lg bg-slate-900 border border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-3 min-w-0">
            <div className="p-2 rounded bg-slate-800 border border-slate-700">
              {getFileIcon(selectedFile.name)}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-white truncate max-w-xs sm:max-w-md">
                {selectedFile.name}
              </p>
              <div className="flex items-center space-x-2 text-[10px] text-slate-400 font-mono mt-0.5">
                <span>{formatFileSize(selectedFile.size)}</span>
                <span>•</span>
                <span className="text-emerald-400 flex items-center space-x-1">
                  <CheckCircle className="w-3 h-3" />
                  <span>Ready for security guard inspection</span>
                </span>
              </div>
            </div>
          </div>

          <button
            type="button"
            onClick={(e) => {
              e.stopPropagation();
              onFileSelect(null);
              if (fileInputRef.current) fileInputRef.current.value = '';
            }}
            disabled={disabled}
            className="p-1.5 rounded-md hover:bg-slate-800 text-slate-400 hover:text-rose-400 transition-colors"
            title="Remove file"
          >
            <X className="w-4 h-4" />
          </button>
        </div>
      )}

      {/* Validation Error */}
      {uploadError && (
        <div className="mt-2 p-2 rounded bg-rose-950/80 border border-rose-800/60 flex items-center space-x-2 text-xs text-rose-300">
          <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0" />
          <span>{uploadError}</span>
        </div>
      )}

      {/* Technical Guard Note */}
      <p className="text-[10px] text-slate-500 mt-1.5 flex flex-wrap items-center gap-1 font-mono">
        <span>🔒 Backend inspects true file magic bytes (%PDF, PNG, JPEG headers) to reject disguised binaries.</span>
      </p>
    </div>
  );
};
