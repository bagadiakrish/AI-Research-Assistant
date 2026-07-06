import { useState } from "react";
import API from "../services/api";
function UploadBox() {

    const [file, setFile] = useState(null);
    const [message, setMessage] = useState("");
    const [loading, setLoading] = useState(false);
    async function uploadFile() {

    if (!file) {
        setMessage("Please choose a PDF first.");
        return;
    }

    const formData = new FormData();

    formData.append("file", file);

    try {

        setLoading(true);

        await API.post("/upload", formData);

        setMessage("✅ PDF uploaded successfully!");

    } catch (e) {

        setMessage("❌ Upload Failed. Please try again.");

    } finally {

        setLoading(false);

    }
    }
    return (

        <div className="upload-box">

            <h2>Upload PDF</h2>

            <input
                type="file"
                onChange={(e) => setFile(e.target.files[0])}
            />

            <button onClick={uploadFile} disabled={loading}>
                {loading ? "Uploading..." : "Upload"}
            </button>
            <p>{message}</p>
        </div>

    );

}

export default UploadBox;