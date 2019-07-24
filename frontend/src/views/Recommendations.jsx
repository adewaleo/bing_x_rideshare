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
// import { Container, Row, Col } from "reactstrap";

// core components
import DemoNavbar from "components/Navbars/DemoNavbar.jsx";
import CardsFooter from "components/Footers/CardsFooter.jsx";

import RecommendationsTitle from "./RecommendationsTitle.jsx";
import RecommendationsListView from "./RecommendationsListView.jsx";

class Recommendations extends React.Component {
  render() {
    return (
      <>
        <DemoNavbar />
        <main ref="main">
          <RecommendationsTitle />
          <RecommendationsListView />
        </main>
        <CardsFooter />
      </>
    );
  }
}

export default Recommendations;
