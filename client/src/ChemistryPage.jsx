import React, { useState } from "react";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Button from "react-bootstrap/Button";
import axios from "axios";
import Spinner from "react-bootstrap/Spinner";
import QAModal from "./QAModal";
import Container from "react-bootstrap/Container";
import Row from "react-bootstrap/Row";
import Col from "react-bootstrap/Col";
import MoleculeCard from "./MoleculeCard";

const CHEMISTRY_SOURCES = ["sample_text_chemistry.txt"];

function ChemistryPage() {
  const [selectedSource, setSelectedSource] = useState(CHEMISTRY_SOURCES[0]);
  const [sourceInformation, setSourceInformation] = useState({});
  const [isCurrentlyFetchingInformation, setIsCurrentlyFetchingInformation] =
    useState(false);

  const handleSelect = (_, event) => {
    setSelectedSource(event.target.value);
  };

  const fetchData = () => {
    const data = {
      source: selectedSource,
    };

    const headers = {
      "Content-Type": "application/json",
    };

    setIsCurrentlyFetchingInformation(true);
    axios
      .post("http://127.0.0.1:5000/api/v1/chemistry/", data, headers)
      .then((response) => {
        setIsCurrentlyFetchingInformation(false);
        setSourceInformation(response.data);
        console.log(response.data);
      })
      .catch((err) => {
        console.log(err);
        setIsCurrentlyFetchingInformation(false);
      });
  };

  return (
    <div className="centeredDiv">
      <div style={{ display: "flex" }}>
        {sourceInformation.summary && <QAModal subject={"chemistry"} />}
        <DropdownButton
          variant="secondary"
          title={selectedSource}
          style={{ marginInlineEnd: 10 }}
        >
          {CHEMISTRY_SOURCES.map((item, index) => {
            return (
              <Dropdown.Item
                onSelect={handleSelect}
                key={index}
                eventKey={item}
              >
                {item}
              </Dropdown.Item>
            );
          })}
        </DropdownButton>

        <Button
          variant="primary"
          disabled={isCurrentlyFetchingInformation}
          onClick={fetchData}
        >
          {isCurrentlyFetchingInformation && (
            <Spinner as="span" size="sm" animation="grow" />
          )}
          {isCurrentlyFetchingInformation ? (
            <span> Generating...</span>
          ) : (
            <span>Generate</span>
          )}
        </Button>
      </div>
      {sourceInformation.summary && (
        <ChemistryContent
          summary={sourceInformation.summary}
          molecules={sourceInformation.molecules}
        />
      )}
    </div>
  );
}

function ChemistryContent({ summary, molecules }) {
  return (
    <Container style={{ padding: 0 }}>
      <Row>
        <Col>
          <div className="centeredDiv" style={{ height: "100%" }}>
            <h3>Key Molecules</h3>
            {molecules.map((molecule) => (
              <MoleculeCard molecule={molecule} />
            ))}
          </div>
        </Col>
        <Col lg={9}>
          <div style={{ whiteSpace: "pre-line" }}>
            <h3>Summary</h3>
            {summary}
          </div>
        </Col>
      </Row>
    </Container>
  );
}

export default ChemistryPage;
