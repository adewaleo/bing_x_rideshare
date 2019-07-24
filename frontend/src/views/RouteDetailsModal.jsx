/*!

=========================================================
* Argon Design System React - v1.0.0
=========================================================

* Product Page: https://www.creative-tim.com/product/argon-design-system-react
* Copyright 2019 Creative Tim (https://www.creative-tim.com)
* Licensed under MIT (https://github.com/creativetimofficial/argon-design-system-react/blob/master/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
import React from "react";

import {
  Button,
  Modal,
} from "reactstrap";

class RouteDetailsModal extends React.Component {
  render() {
    return (
      <>
        <Modal
          className="modal-dialog-centered"
          isOpen={this.props.shouldShow}
          toggle={this.props.toggleModal}
        >
          <div className="modal-header">
            <h6 className="modal-title" id="modal-title-default">
              Option 1
            </h6>
            <button
              aria-label="Close"
              className="close"
              data-dismiss="modal"
              type="button"
              onClick={this.props.toggleModal}
            >
              <span aria-hidden={true}>×</span>
            </button>
          </div>
          <div className="modal-body">
            <section className="section-components">
              <span className="text-uppercase badge badge-primary badge-pill">Quickest</span>
              <span className="text-uppercase badge badge-success badge-pill">Cheapest</span>
              <span className="text-uppercase badge badge-danger badge-pill">Expensive</span>
              <span className="text-uppercase badge badge-warning badge-pill">Slowest</span>
            </section>
            <div>
              <span className="lead" style={{marginRight: "2rem"}}>13:45 - 13:55</span>
              <span className="lead text-muted">10 minutes</span>
              <p className="lead">$3.14</p>
            </div>
            <p>
              Take a bus, car, etc.
            </p>
          </div>
          <div className="modal-footer">
            <Button
              className="ml-auto"
              color="success"
              data-dismiss="modal"
              type="button"
              onClick={this.props.toggleModal}
            >
              Close
            </Button>
          </div>
        </Modal>
      </>
    );
  }
}

export default RouteDetailsModal;
