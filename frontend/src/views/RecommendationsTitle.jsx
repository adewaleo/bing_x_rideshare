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
// reactstrap components
import { Container, Row, Col } from "reactstrap";

class ResultsTitle extends React.Component {
  render() {
    return (
      <>
        <section className="bg-gradient-orange">
          <Container className="pt-lg pb-100">
            <Row className="text-center justify-content-center">
              <Col lg="10">
                <h2 className="display-3 text-white">Recommendations</h2>
                <p className="lead text-white">
                  Here's what we've got for you...
                </p>
              </Col>
            </Row>
          </Container>
        </section>
      </>
    );
  }
}

export default ResultsTitle;
