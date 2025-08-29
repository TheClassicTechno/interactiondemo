
import React, { useState } from "react";

// Main App component for the Email Digest frontend
function App() {
  // State to hold the selected file
  const [file, setFile] = useState<File | null>(null);
  // State to hold the download URL for the generated PDF
  const [downloadUrl, setDownloadUrl] = useState<string | null>(null);

  // Handle file input change
  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) setFile(e.target.files[0]);
  };

  // Handle form submission to generate digest
  const handleSubmit = async () => {
    if (!file) return;
    const formData = new FormData();
    formData.append("file", file);

    // Send file to backend API to generate digest PDF
    const res = await fetch("http://localhost:8000/generate-digest/", {
      method: "POST",
      body: formData
    });

    // Receive PDF as blob and create download URL
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    setDownloadUrl(url);
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "Arial" }}>
      {/* Title and file input */}
      <h1>📨 Morning Email Digest</h1>
      <input type="file" accept=".json" onChange={handleFileChange} />
      <button onClick={handleSubmit} style={{ marginLeft: "1rem" }}>
        Generate Digest
      </button>
      {/* Show download link if PDF is ready */}
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
