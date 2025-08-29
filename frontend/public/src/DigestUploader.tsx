
import { useState } from "react";

// DigestUploader component: Handles uploading emails, generating digest, and PDF preview/download
export default function DigestUploader() {
  // State for the digest text
  const [digest, setDigest] = useState<string>("");
  // State for the uploaded file
  const [file, setFile] = useState<File | null>(null);
  // State for the generated PDF URL
  const [pdfUrl, setPdfUrl] = useState<string>("");

  // Handle file input change
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) setFile(e.target.files[0]);
  };

  // Fetch digest summary from backend
  const fetchDigest = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    // POST file to backend to get digest summary
    const res = await fetch("http://localhost:8000/digest", { method: "POST", body: formData });
    const data = await res.json();
    setDigest(data.digest);
    setPdfUrl(""); // reset PDF preview
  };

  // Download and preview PDF from backend
  const downloadPDF = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    // POST file to backend to get PDF
    const res = await fetch("http://localhost:8000/digest/pdf", { method: "POST", body: formData });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    setPdfUrl(url);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      {/* Title and file input */}
      <h1>📨 Upload Emails JSON</h1>
      <input type="file" accept=".json" onChange={handleFileChange} />
      <div style={{ marginTop: "1rem" }}>
        <button onClick={fetchDigest} style={{ marginRight: "1rem" }}>Generate Digest</button>
        <button onClick={downloadPDF}>Generate & Preview PDF</button>
      </div>

      {/* Show digest summary if available */}
      {digest && (
        <pre style={{ backgroundColor: "#f5f5f5", padding: "1rem", borderRadius: "5px", marginTop: "1rem" }}>
          {digest}
        </pre>
      )}

      {/* Show PDF preview and download link if available */}
      {pdfUrl && (
        <div style={{ marginTop: "1rem" }}>
          <h2>📄 PDF Preview</h2>
          <iframe src={pdfUrl} width="100%" height="600px" title="PDF Preview"></iframe>
          <a href={pdfUrl} download={`${file?.name}.pdf`} style={{ display: "block", marginTop: "1rem" }}>
            ⬇️ Download PDF
          </a>
        </div>
      )}
    </div>
  );
}
