import React, { useState } from "react";
import Form from "react-bootstrap/Form";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import { ImPencil2, ImCross } from "react-icons/im";
import { GoCheck } from "react-icons/go";

export default function QuizModal({ quiz }) {
  const [showModal, setShowModal] = useState(false);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [currentSelectedOption, setCurrentSelectedOption] = useState(null);
  const [showResults, setShowResults] = useState(false);

  const onQuizButtonPress = () => setShowModal(true);
  const onHide = () => setShowModal(false);

  const handleNext = () => {
    setCurrentQuestionIndex(currentQuestionIndex + 1);
    setShowResults(false);
    setCurrentSelectedOption(null);
  };

  const handlePrevious = () => {
    setCurrentQuestionIndex(currentQuestionIndex - 1);
    setShowResults(false);
    setCurrentSelectedOption(null);
  };

  const currentQuestion = quiz[currentQuestionIndex];
  console.log(currentSelectedOption);
  return (
    <>
      <Button
        style={{ position: "fixed", right: 30, bottom: 100, zIndex: 1 }}
        size="lg"
        variant="primary"
        className="rounded-circle"
        onClick={onQuizButtonPress}
      >
        <ImPencil2 />
      </Button>
      <Modal
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
        show={showModal}
        onHide={onHide}
      >
        <Modal.Header closeButton>
          <Modal.Title>Test your knowledge</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <h4>{currentQuestion.question}</h4>
          <Form>
            {currentQuestion.options.map((option, index) => {
              return (
                <div style={{ display: "flex" }}>
                  <Form.Check
                    key={`${currentQuestionIndex}_${index}`}
                    label={option}
                    type="radio"
                    name={`group_${currentQuestionIndex}`}
                    id="default radio"
                    onClick={() => setCurrentSelectedOption(index)}
                  />
                  <div style={{ marginLeft: 10 }}>
                    {showResults &&
                      (currentQuestion.answer == index ? (
                        <GoCheck color="green" size="1.3em" />
                      ) : (
                        <ImCross color="red" />
                      ))}
                  </div>
                </div>
              );
            })}
          </Form>
          <p align="center">
            Question {currentQuestionIndex + 1} of {quiz.length}
          </p>
          <div
            className="centeredDiv"
            style={{ flexDirection: "row", justifyContent: "center" }}
          >
            <Button
              className="QuizButton"
              onClick={handlePrevious}
              disabled={currentQuestionIndex == 0}
            >
              Previous
            </Button>
            <Button
              disabled={currentSelectedOption == null}
              className="QuizButton"
              onClick={() => setShowResults(true)}
            >
              Submit
            </Button>
            <Button
              className="QuizButton"
              onClick={handleNext}
              disabled={currentQuestionIndex == quiz.length}
            >
              Next
            </Button>
          </div>
        </Modal.Body>
      </Modal>
    </>
  );
}
