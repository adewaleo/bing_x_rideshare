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
import RecommendationsListViewItem from "./RecommendationsListViewItem";
import { Row, Col } from "reactstrap";

class RecommendationsListView extends React.Component {
  constructor(props) {
    super(props);
    this.route = {id: "1234", segments: [{mode: "transit"}]};
  }

  render() {
    return (
      <>
      <Row className="py-md align-items-center">
        <Col lg="12">
          <RecommendationsListViewItem route={this.route} />
          <RecommendationsListViewItem route={this.route} />
          <RecommendationsListViewItem route={this.route} />
        </Col>
      </Row>
      </>
    );
  }
}

export default RecommendationsListView;
