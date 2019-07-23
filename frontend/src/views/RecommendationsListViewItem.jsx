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
import { Card,
  CardBody,
  // NavItem,
  // NavLink,
  // Nav,
  // TabContent,
  // TabPane,
  Container,
  Row,
  // Col
} from "reactstrap";

class RecommendationsListViewItem extends React.Component {
  render() {
    return (
      <>
        <Container>
          <Row className="py-3 align-items-center">
            <Card className="shadow" style={{margin: "0 auto"}}>
              <CardBody>
                <p className="description">
                  Choose this option if you want us to optimize for time.
                  This may mean that your costs may be slightly higher.
                </p>
              </CardBody>
            </Card>
          </Row>
        </Container>
      </>
    );
  }
}

export default RecommendationsListViewItem;
