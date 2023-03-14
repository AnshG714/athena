import "./App.css";

function SubjectCard({ subjectName }) {
  return (
    <button
      className="SubjectCard"
      style={{
        border: "none",
        cursor: "pointer",
        outline: "none",
        fontSize: 20,
      }}
    >
      {subjectName}
    </button>
  );
}

function App() {
  return (
    <div className="App">
      <h3 style={{ textAlign: "center", fontWeight: "normal" }}>
        Welcome! Please select a subject to get started.
      </h3>
      <div style={{ display: "flex", justifyContent: "center" }}>
        <SubjectCard subjectName="History" />
        <SubjectCard subjectName="History" />
        <SubjectCard subjectName="History" />
      </div>
    </div>
  );
}

export default App;
