import { useState } from "react";

export default function DigestUploader() {
  const [digest, setDigest] = useState<string>("");
  const [file, setFile] = useState<File | null>(null);
  const [pdfUrl, setPdfUrl] = useState<string>("");

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.length) setFile(e.target.files[0]);
  };

  const fetchDigest = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/digest", { method: "POST", body: formData });
    const data = await res.json();
    setDigest(data.digest);
    setPdfUrl(""); // reset PDF preview
  };

  const downloadPDF = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/digest/pdf", { method: "POST", body: formData });
    const blob = await res.blob();
    const url = window.URL.createObjectURL(blob);
    setPdfUrl(url);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>📨 Upload Emails JSON</h1>
      <input type="file" accept=".json" onChange={handleFileChange} />
      <div style={{ marginTop: "1rem" }}>
        <button onClick={fetchDigest} style={{ marginRight: "1rem" }}>Generate Digest</button>
        <button onClick={downloadPDF}>Generate & Preview PDF</button>
      </div>

      {digest && (
        <pre style={{ backgroundColor: "#f5f5f5", padding: "1rem", borderRadius: "5px", marginTop: "1rem" }}>
          {digest}
        </pre>
      )}

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
