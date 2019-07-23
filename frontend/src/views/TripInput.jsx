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
// nodejs library that concatenates classes
// import classnames from "classnames";

// reactstrap components
import { FormGroup,
  Input,
  Container,
  Row,
  Col } from "reactstrap";

  import TripInputTabs from "./TripInputTabs.jsx";


class TripInput extends React.Component {
  render() {
    return (
      <>
          <Container>
            <Row className="py-3 align-items-center">
                <h3 className="heading-title mb-0">
                  Enter your trip
                </h3>
            </Row>
            <Row className="py-3 align-items-center">
              {/* <Col sm="3">
                <h2>
                  Start
                </h2>
              </Col> */}
              <FormGroup>
                  <Input placeholder="Start" type="text" />
                </FormGroup>
            </Row>
            <Row className="py-3 align-items-center">
              {/* <Col sm="3">
                <h2>
                  Destination
                </h2>
              </Col> */}
              <FormGroup>
                  <Input placeholder="Destination" type="text" />
                </FormGroup>
            </Row>
            <Row className="py-3 align-items-center">
              <TripInputTabs />
            </Row>
          </Container>
      </>
    );
  }
}

export default TripInput;
