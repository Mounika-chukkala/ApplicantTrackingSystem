import { useState } from "react";
import axios from "axios";

export default function App() {
  const [jobDescription, setJobDescription] = useState("");
  const [file, setFile] = useState(null);
  const [response, setResponse] = useState("");

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (endpoint) => {
    if (!file) {
      alert("Please upload a resume");
      return;
    }
    
    const formData = new FormData();
    formData.append("job_description", jobDescription);
    formData.append("resume", file);
    
    try {
      const res = await axios.post(`http://localhost:8000/${endpoint}`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setResponse(res.data);
    } catch (error) {
      setResponse("Error processing request");
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
      <h1 className="text-2xl font-bold mb-4">ATS Resume Expert</h1>
      <textarea
        className="w-full max-w-lg p-2 border rounded"
        placeholder="Enter Job Description"
        value={jobDescription}
        onChange={(e) => setJobDescription(e.target.value)}
      />
      <input
        type="file"
        accept=".pdf"
        className="my-4"
        onChange={handleFileChange}
      />
      <div className="flex space-x-2">
        <button
          className="bg-blue-500 text-white px-4 py-2 rounded"
          onClick={() => handleSubmit("evaluate")}
        >
          Tell me about the Resume
        </button>
        <button
          className="bg-green-500 text-white px-4 py-2 rounded"
          onClick={() => handleSubmit("match_percentage")}
        >
          Percentage Match
        </button>
      </div>
      <div className="mt-4 p-4 bg-white shadow rounded w-full max-w-lg">
        <h2 className="text-lg font-semibold">Response:</h2>
        <p>{response}</p>
      </div>
    </div>
  );
}
