import React, { useState } from "react";

function App() {
  const [file, setFile] = useState<File | null>(null);
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setFile(e.target.files[0]);
  };

  const handleSubmit = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch("http://localhost:8000/generate-digest/", {
      method: "POST",
      body: formData
    });

    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    setDownloadUrl(url);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      <h1>📨 Morning Email Digest</h1>
      <input type="file" accept=".json" onChange={handleFileChange} />
      <button onClick={handleSubmit} style={{ marginLeft: "1rem" }}>
        Generate Digest
      </button>
      {downloadUrl && (
        <div style={{ marginTop: "1rem" }}>
          <a href={downloadUrl} download="morning_digest.pdf">
            Download PDF
          </a>
        </div>
      )}
    </div>
  );
}

export default App;
