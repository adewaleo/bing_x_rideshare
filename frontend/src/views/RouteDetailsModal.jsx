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
  Row,
  Card,
  CardBody,
  Container
} from "reactstrap";

import RouteDetailsSegment from "./RouteDetailsSegment.jsx";

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
              <span className="text-uppercase badge badge-success badge-pill">Save 15 mins</span>
              <span className="text-uppercase badge badge-primary badge-pill">Moderate cost</span>
              {/* <span className="text-uppercase badge badge-danger badge-pill">Expensive</span>
              <span className="text-uppercase badge badge-warning badge-pill">Slowest</span> */}
            </section>
            <div>
              <span className="lead" style={{marginRight: "2rem"}}>18:15 - 18:41</span>
              <span className="text-muted">26 minutes</span>
              <p className="lead">$8.25</p>
            </div>
            <hr />
            <h6>Trip details</h6>
            {/* <RouteDetailsSegment />
            <RouteDetailsSegment /> */}
            <Container>
              <Row>
                <Card style={{minWidth: '100%'}}>
                  <CardBody>
                    <i className="fa fa-female" style={{fontSize: "2rem"}} />
                    <span className="lead" style={{marginLeft: "1rem"}}>4 minutes</span>
                    <span className="lead"> | </span>
                    <span className="lead">Walk</span>
                    {/* <span className="lead"> | </span>
                    <span className="lead">$2.95</span> */}
                    <p>Walk to Greenwood Ave N & N 92nd St</p>
                  </CardBody>
                </Card>
              </Row>
            </Container>
            <Container>
              <Row>
                <Card style={{minWidth: '100%'}}>
                  <CardBody>
                    <i className="fa fa-bus" style={{fontSize: "2rem"}} />
                    <span className="lead" style={{marginLeft: "1rem"}}>15 minutes</span>
                    <span className="lead"> | </span>
                    <span className="lead">Transit</span>
                    <span className="lead"> | </span>
                    <span className="lead">$2.75</span>
                    <p>Take the 5 bus - Downtown Seattle Greenwood and get off at Aurora Ave N & Denny Way</p>
                  </CardBody>
                </Card>
              </Row>
            </Container>
            <Container>
              <Row>
                <Card style={{minWidth: '100%'}}>
                  <CardBody>
                    <i className="fa fa-car" style={{fontSize: "2rem"}} />
                    <span className="lead" style={{marginLeft: "1rem"}}>7 minutes</span>
                    <span className="lead"> | </span>
                    <span className="lead">Rideshare</span>
                    <span className="lead"> | </span>
                    <span className="lead">$5.50</span>
                    <p>Walk to the Space Needle</p>
                  </CardBody>
                </Card>
              </Row>
            </Container>
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
