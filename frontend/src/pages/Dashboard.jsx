import { useState } from "react";

function Dashboard() {
  const [resume, setResume] = useState(null);
  const [jobDesc, setJobDesc] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!resume || !jobDesc) {
      alert("Upload resume and enter job description");
      return;
    }

    const formData = new FormData();
    formData.append("resume", resume);
    formData.append("job_description", jobDesc);

    setLoading(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/analyze/", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Analysis failed");
      }

      const data = await res.json();
      setResult(data);
    } catch (err) {
      alert(err.message);
    } finally {
      setLoading(false);
    }
  };

  const score = result?.ats_score || 0;

  return (
    <div style={styles.page}>
      {/* HEADER */}
      <h1 style={styles.title}>Resume Analyzer</h1>
      <p style={styles.subtitle}>
        Upload your resume and job description to identify skill gaps
      </p>

      {/* INPUT SECTION */}
      <div style={styles.inputGrid}>
        {/* RESUME UPLOAD */}
        <div style={styles.uploadCard}>
          <h3>Upload Resume</h3>

          <label style={styles.uploadBox}>
            <input
              type="file"
              accept=".pdf,.docx"
              hidden
              onChange={(e) => setResume(e.target.files[0])}
            />

            <p style={styles.uploadText}>
              {resume ? resume.name : "Drag & drop your resume here"}
            </p>

            <p style={styles.muted}>
              or click to browse • PDF / DOCX • Max 10MB
            </p>
          </label>
        </div>

        {/* JOB DESCRIPTION */}
        <div style={styles.card}>
          <h3>Job Description</h3>
          <textarea
            placeholder="Paste the full job description here..."
            value={jobDesc}
            onChange={(e) => setJobDesc(e.target.value)}
            rows={12}
            style={styles.textarea}
          />
        </div>
      </div>

      {/* ANALYZE BUTTON */}
      <div style={styles.center}>
        <button onClick={handleAnalyze} style={styles.analyzeBtn}>
          {loading ? "Analyzing..." : "Analyze Resume"}
        </button>
      </div>

      {/* RESULTS */}
      {result && (
        <div style={styles.resultGrid}>
          {/* ATS SCORE */}
          <div style={styles.cardCenter}>
            <svg width="160" height="160">
              <circle
                cx="80"
                cy="80"
                r="70"
                stroke="#e5e7eb"
                strokeWidth="10"
                fill="none"
              />
              <circle
                cx="80"
                cy="80"
                r="70"
                stroke="#111827"
                strokeWidth="10"
                fill="none"
                strokeDasharray="440"
                strokeDashoffset={440 - (440 * score) / 100}
                strokeLinecap="round"
              />
              <text
                x="50%"
                y="50%"
                dominantBaseline="middle"
                textAnchor="middle"
                fontSize="26"
                fontWeight="600"
                fill="#111827"
              >
                {score}%
              </text>
            </svg>
            <p style={{ marginTop: "10px", fontWeight: 600 }}>ATS Score</p>
          </div>

          {/* MATCHED SKILLS */}
          <div style={styles.card}>
            <h3>Matched Skills</h3>
            <ul>
              {result.matched_skills.map((s, i) => (
                <li key={i} style={styles.match}>{s}</li>
              ))}
            </ul>
          </div>

          {/* MISSING SKILLS */}
          <div style={styles.card}>
            <h3>Missing Skills</h3>
            <ul>
  {(result?.missing_skills || []).map((s, i) => (
    <li key={i} style={styles.miss}>{s}</li>
  ))}
</ul>

          </div>
        </div>
      )}
    </div>
  );
}

export default Dashboard;

/* ===================== STYLES ===================== */

const styles = {
  page: {
    background: "#f9fafb",
    minHeight: "100vh",
    padding: "40px",
    maxWidth: "1200px",
    margin: "0 auto",
    color: "#111827",
  },

  title: {
    textAlign: "center",
    fontSize: "34px",
    fontWeight: 700,
  },

  subtitle: {
    textAlign: "center",
    color: "#6b7280",
    marginBottom: "40px",
  },

  inputGrid: {
    display: "grid",
    gridTemplateColumns: "1.5fr 1fr",
    gap: "30px",
    alignItems: "stretch",
  },

  uploadCard: {
    background: "#ffffff",
    borderRadius: "16px",
    padding: "30px",
    border: "1px solid #e5e7eb",
  },

  uploadBox: {
    border: "2px dashed #d1d5db",
    borderRadius: "14px",
    padding: "90px 40px",
    textAlign: "center",
    cursor: "pointer",
    marginTop: "20px",
    display: "flex",
    flexDirection: "column",
    justifyContent: "center",
    gap: "10px",
  },

  uploadText: {
    fontSize: "18px",
    fontWeight: 600,
  },

  muted: {
    color: "#6b7280",
    fontSize: "14px",
  },

  card: {
    background: "#ffffff",
    borderRadius: "16px",
    padding: "25px",
    border: "1px solid #e5e7eb",
  },

  cardCenter: {
    background: "#ffffff",
    borderRadius: "16px",
    padding: "25px",
    border: "1px solid #e5e7eb",
    textAlign: "center",
  },

  textarea: {
    width: "100%",
    padding: "14px",
    borderRadius: "10px",
    border: "1px solid #d1d5db",
    marginTop: "10px",
    resize: "none",
    fontSize: "14px",
  },

  center: {
    textAlign: "center",
    marginTop: "35px",
  },

  analyzeBtn: {
    background: "#111827",
    color: "white",
    padding: "14px 34px",
    borderRadius: "12px",
    border: "none",
    fontSize: "16px",
    cursor: "pointer",
    fontWeight: 600,
  },

  resultGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))",
    gap: "25px",
    marginTop: "50px",
  },

  match: {
    color: "#065f46",
    fontWeight: 500,
  },

  miss: {
    color: "#991b1b",
    fontWeight: 500,
  },
};
