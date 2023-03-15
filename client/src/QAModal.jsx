import React, { useState } from "react";
import axios from "axios";
import Modal from "react-bootstrap/Modal";
import Form from "react-bootstrap/Form";
import Button from "react-bootstrap/Button";
import Spinner from "react-bootstrap/Spinner";
import { BsChatRightDots } from "react-icons/bs";

export default function QAModal({ subject }) {
  const [showModal, setShowModal] = useState(false);
  const [currentText, setCurrentText] = useState("");
  const [isCurrentlyFetching, setIsCurrentlyFetching] = useState(false);
  const [answer, setAnswer] = useState("");

  const onHide = () => setShowModal(false);
  const onButtonPress = () => setShowModal(true);
  const onTextChange = (e) => setCurrentText(e.target.value);

  const constructUrl = () => `http://127.0.0.1:5000/api/v1/${subject}/qa`;

  const getAnswerForQuery = () => {
    if (!currentText) {
      return;
    }

    const data = { query: currentText };
    const headers = {
      "Content-Type": "application/json",
    };

    setIsCurrentlyFetching(true);
    axios
      .post(constructUrl(), data, headers)
      .then((response) => {
        setIsCurrentlyFetching(false);
        console.log(response.data.answer);
        setAnswer(response.data.answer);
        console.log(response.data);
      })
      .catch((err) => {
        console.log(err);
        setIsCurrentlyFetching(false);
      });
  };

  return (
    <>
      <Button
        style={{ position: "fixed", right: 30, bottom: 30, zIndex: 1 }}
        size="lg"
        variant="primary"
        className="rounded-circle"
        onClick={onButtonPress}
      >
        <BsChatRightDots />
      </Button>
      <Modal
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
        show={showModal}
        onHide={onHide}
      >
        <Modal.Header closeButton>
          <Modal.Title>Ask a question about this text!</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <Form
            onSubmit={(e) => {
              e.preventDefault();
            }}
          >
            <Form.Group className="mb-3" controlId="exampleForm.ControlInput1">
              <Form.Control
                value={currentText}
                onChange={onTextChange}
                type="text"
                placeholder="Ask a question"
              />
            </Form.Group>
          </Form>
          <div className="centeredDiv">
            <Button
              style={{ width: "30%", borderRadius: 30, marginBottom: 10 }}
              disabled={isCurrentlyFetching}
              onClick={getAnswerForQuery}
            >
              {isCurrentlyFetching && (
                <Spinner as="span" size="sm" animation="grow" />
              )}
              {isCurrentlyFetching ? <span> Getting right back to you</span> : <span>Ask</span>}
            </Button>
          </div>
          {answer && <p>{answer}</p>}
        </Modal.Body>
      </Modal>
    </>
  );
}
