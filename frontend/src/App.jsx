import { useState } from 'react';
import axios from 'axios';

function App() {
  const [formData, setFormData] = useState({
    training_title: '',
    repository_link: '',
    sharepoint_link: '',
  });

  const [files, setFiles] = useState({
    attendance: [],
    qna: [],
    transcript: [],
    feedback: [],
  });

  const handleChange = (e) => {
    setFormData({...formData, [e.target.name]: e.target.value});
  };

  const handleFileChange = (e, key) => {
    setFiles({...files, [key]: e.target.files});
  };

  // const handleSubmit = async (e) => {
  //   e.preventDefault();
  //   const data = new FormData();
  //   for (let key in formData) {
  //     data.append(key, formData[key]);
  //   }
  //   for (let type in files) {
  //     for (let file of files[type]) {
  //       data.append(type, file);
  //     }
  //   }

  //   try {
  //     const response = await axios.post('http://localhost:5000/process', data, {
  //       responseType: 'blob'
  //     });

  //     const blob = new Blob([response.data]);
  //     const url = window.URL.createObjectURL(blob);
  //     const a = document.createElement('a');
  //     a.href = url;
  //     a.download = "summary_email.eml";
  //     a.click();
  //   } catch (err) {
  //     alert("Error: " + err.response?.data?.error || err.message);
  //   }
  // };
  const handleSubmit = async (e) => {
  e.preventDefault();
  const data = new FormData();
  for (let key in formData) {
    data.append(key, formData[key]);
  }
  for (let type in files) {
    for (let file of files[type]) {
      data.append(type, file);
    }
  }

  try {
    // First request: get the JSON response with the file URLs
    const response = await axios.post('http://localhost:5000/process', data);
    const emlUrl = 'http://localhost:5000' + response.data.files.eml_path;

    // Second request: download the EML as blob
    const emlBlob = await axios.get(emlUrl, { responseType: 'blob' });
    const url = window.URL.createObjectURL(new Blob([emlBlob.data]));
    const a = document.createElement('a');
    a.href = url;
    a.download = "summary_email.eml";
    document.body.appendChild(a);
    a.click();
    a.remove();

  } catch (err) {
    alert("Error: " + (err.response?.data?.error || err.message));
  }
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h2>Training Session Summary Generator</h2>
      <form onSubmit={handleSubmit}>
        <input type="text" name="training_title" placeholder="Training Title" onChange={handleChange} required /><br />
        <input type="text" name="repository_link" placeholder="Repository Link" onChange={handleChange} required /><br />
        <input type="text" name="sharepoint_link" placeholder="SharePoint Link" onChange={handleChange} required /><br /><br />

        <label>Attendance CSV:</label>
        <input type="file" multiple onChange={(e) => handleFileChange(e, "attendance")} /><br />
        <label>Q&A CSV:</label>
        <input type="file" multiple onChange={(e) => handleFileChange(e, "qna")} /><br />
        <label>Transcript VTT:</label>
        <input type="file" multiple onChange={(e) => handleFileChange(e, "transcript")} /><br />
        <label>Feedback Excel:</label>
        <input type="file" multiple onChange={(e) => handleFileChange(e, "feedback")} /><br /><br />

        <button type="submit">Generate Summary</button>
      </form>
    </div>
  );
}

export default App;

