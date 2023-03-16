import React, { useState } from "react";
import Modal from "react-bootstrap/Modal";
import MoleculeRenderer from "./MoleculeRenderer";

function MoleculeCard({ molecule }) {
  const [showModal, setShowModal] = useState(false);
  const onHide = () => setShowModal(false);
  const onShow = () => setShowModal(true);

  return (
    <>
      <Modal
        show={showModal}
        onHide={onHide}
        size="lg"
        aria-labelledby="contained-modal-title-vcenter"
        centered
      >
        <Modal.Header closeButton>
          <Modal.Title>
            {molecule.molecule_name}
            {constructChemicalFormula(molecule.chemical_formula)}
          </Modal.Title>
        </Modal.Header>
        <Modal.Body>
          <MoleculeRenderer moleculeJSON={molecule.molecular_structure} />
        </Modal.Body>
      </Modal>
      <div className="MoleculeCard" onClick={onShow}>
        <h4 align="center">{molecule.molecule_name}</h4>
        <p align="center">
          {constructChemicalFormula(molecule.chemical_formula)}
        </p>
      </div>
    </>
  );
}

function constructChemicalFormula(moleculeName) {
  const spans = [];
  for (var i = 0; i < moleculeName.length; i++) {
    if (!isNaN(moleculeName[i])) {
      spans.push(<sub>{moleculeName[i]}</sub>);
    } else {
      spans.push(<span>{moleculeName[i]}</span>);
    }
  }

  return <p>{spans}</p>;
}

export default MoleculeCard;
