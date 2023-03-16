import React, { useState } from "react";
import Dropdown from "react-bootstrap/Dropdown";
import DropdownButton from "react-bootstrap/DropdownButton";
import Button from "react-bootstrap/Button";
import axios from "axios";
import Spinner from "react-bootstrap/Spinner";
import Carousel from "react-bootstrap/Carousel";
import QAModal from "./QAModal";
import background from "./images/background.jpg";

const HISTORY_SOURCES = ["sample_text_history.txt"];

function HistoryPage() {
  const [selectedSource, setSelectedSource] = useState(HISTORY_SOURCES[0]);
  const [sourceInformation, setSourceInformation] = useState({});
  const [isCurrentlyFetchingInformation, setIsCurrentlyFetchingInformation] =
    useState(false);

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
        {sourceInformation.summary && <QAModal subject={"history"} />}
        <DropdownButton
          variant="secondary"
          title={selectedSource}
          style={{ marginInlineEnd: 10 }}
        >
          {HISTORY_SOURCES.map((item, index) => {
            return (
              <Dropdown.Item
                onSelect={() => setSelectedSource(item)}
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
        <HistoryContent
          summary={sourceInformation.summary}
          timeline={sourceInformation.timeline}
        />
      )}
    </div>
  );
}

function HistoryContent({ summary, timeline }) {
  console.log(timeline);
  return (
    <div style={{ whiteSpace: "pre-line" }}>
      <h3>Summary</h3>
      {summary}
      <h3>Timeline</h3>
      <Carousel variant="dark">
        {timeline.map((event) => (
          <Carousel.Item key={event.event}>
            <img src={background} width={100} height={300} className=" w-100" />
            <Carousel.Caption>
              <h3 style={{ color: "blue" }}>{event.date}</h3>
              <p>{event.event}</p>
            </Carousel.Caption>
          </Carousel.Item>
        ))}
      </Carousel>
    </div>
  );
}

export default HistoryPage;
