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
  Row,
  Card,
  CardBody,
  Container
} from "reactstrap";

class RouteDetailsSegment extends React.Component {
  render() {
    return (
      <>
        <Container>
          <Row>
            <Card style={{minWidth: '100%'}}>
              <CardBody>
                <i className="fa fa-car" style={{fontSize: "2rem"}} />
                <span className="lead" style={{marginLeft: "1rem"}}>4 minutes</span>
                <span className="lead"> | </span>
                <span className="lead">Rideshare</span>
                <span className="lead"> | </span>
                <span className="lead">$3.14</span>
                <p>Take a rideshare from Main Street to Clifton Street</p>
              </CardBody>
            </Card>
          </Row>
        </Container>
      </>
    );
  }
}

export default RouteDetailsSegment;
