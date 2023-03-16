import React from "react";
import "./App.css";
import { BrowserRouter, Routes, Route, Link } from "react-router-dom";
import HistoryPage from "./HistoryPage";
import ChemistryPage from "./ChemistryPage";

const SUBJECTS = ["History", "Chemistry", "Computer Science"];

function SubjectCard({ subjectName }) {
  const link = `/${subjectName.toLowerCase().replace(" ", "-")}`;
  return (
    <Link to={link}>
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
    </Link>
  );
}

function Home() {
  return (
    <div className="App">
      <h3 style={{ textAlign: "center", fontWeight: "normal" }}>
        Welcome! Please select a subject to get started.
      </h3>
      <div style={{ display: "flex", justifyContent: "center" }}>
        {SUBJECTS.map((subject) => (
          <SubjectCard subjectName={subject} />
        ))}
      </div>
    </div>
  );
}

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" exact element={<Home />} />
        <Route path="/history" element={<HistoryPage />} />
        <Route path="/computer-science" element={<div>CS page</div>} />
        <Route path="/chemistry" element={<ChemistryPage />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
