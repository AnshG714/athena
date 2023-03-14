import React, { useState } from "react";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Button from "react-bootstrap/Button";
import axios from "axios";
import Spinner from "react-bootstrap/Spinner";

const HISTORY_SOURCES = ["sample_text_history.txt"];

function HistoryPage() {
  const [selectedSource, setSelectedSource] = useState(HISTORY_SOURCES[0]);
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
      .post("http://127.0.0.1:5000/api/v1/history/", data, headers)
      .then((response) => {
        setIsCurrentlyFetchingInformation(false);
        console.log(response);
      })
      .catch((err) => {
        console.log(err);
        setIsCurrentlyFetchingInformation(false);
      });
  };

  return (
    <div className="centeredDiv">
      <div style={{ display: "flex" }}>
        <DropdownButton
          variant="secondary"
          onSelect={handleSelect}
          title={selectedSource}
          style={{ marginInlineEnd: 10 }}
        >
          {HISTORY_SOURCES.map((item, index) => {
            return (
              <Dropdown.Item key={index} eventKey={item}>
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
      {sourceInformation.summary && <HistoryContent />}
    </div>
  );
}

function HistoryContent() {}

export default HistoryPage;
