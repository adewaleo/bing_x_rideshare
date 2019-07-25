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
    this.route1 = {id: "1", segments: [{mode: "walk"}, {mode: "transit"}, {mode: "rideshare"}], quickest: true, cheapest: true, startTime: "18:15", endTime: "18:41", duration: "26 minutes", cost: "8.25"};
    this.route2 = {id: "2", segments: [{mode: "walk"}, {mode: "transit"}, {mode: "walk"}, {mode: "transit"}], slowest: true, startTime: "18:15", endTime: "18:56", duration: "41 minutes", cost: "2.50"};
  }

  render() {
    return (
      <>
      <Row className="py-md align-items-center">
        <Col lg="12">
          <RecommendationsListViewItem route={this.route1} />
          <RecommendationsListViewItem route={this.route2} />
        </Col>
      </Row>
      </>
    );
  }
}

export default RecommendationsListView;
