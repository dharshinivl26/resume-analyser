export default function ATSProgressBar({ score }) {
  const getColor = () => {
    if (score >= 75) return "#22c55e";   // green
    if (score >= 50) return "#facc15";   // yellow
    return "#ef4444";                    // red
  };

  return (
    <div style={{ width: "400px", marginTop: "20px" }}>
      <p style={{ color: "white", marginBottom: "6px" }}>
        ATS Score: <strong>{score}%</strong>
      </p>

      <div
        style={{
          width: "100%",
          height: "18px",
          backgroundColor: "#1f2937",
          borderRadius: "10px",
          overflow: "hidden",
        }}
      >
        <div
          style={{
            width: `${score}%`,
            height: "100%",
            backgroundColor: getColor(),
            transition: "width 0.6s ease",
          }}
        />
      </div>
    </div>
  );
}
