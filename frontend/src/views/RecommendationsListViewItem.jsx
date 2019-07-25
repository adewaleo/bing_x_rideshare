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
import {
  Button,
  Card,
  CardBody,
  Container,
  Row,
  Col
} from "reactstrap";

import RouteDetailsModal from "./RouteDetailsModal.jsx";

class RecommendationsListViewItem extends React.Component {
  state = {};
  toggleModal = state => {
    this.setState({
      [state]: !this.state[state]
    });
  };

  render() {
    return (
      <>
        <Container>
          <Row className="py-3 align-items-center">
            <Card className="shadow" style={{margin: "0 auto", minWidth: '80%'}}>
              <CardBody>
                <Row className=" align-items-center justify-content-md-between">
                  <Col md="10">
                    <div className="icons-container blur-item on-screen">
                      <h4 className="heading-title text-warning mb-0">Option {this.props.route.id}</h4>
                      <section className="section-components">
                        {this.props.route.cheapest &&
                          <span className="text-uppercase badge badge-success badge-pill">Save 15 mins</span>
                        }
                        {this.props.route.quickest &&
                          <span className="text-uppercase badge badge-primary badge-pill">Moderate cost</span>
                        }
                        {this.props.route.expensive &&
                          <span className="text-uppercase badge badge-danger badge-pill">Expensive</span>
                        }
                        {this.props.route.slowest &&
                          <span className="text-uppercase badge badge-warning badge-pill">Cheapest</span>
                        }
                      </section>
                      <ul style={{margin: 0, padding: "1rem 0"}}>
                        {this.props.route.segments.map((segment) =>
                        <li key={segment.toString()} value={segment} style={{listStyleType: 'none', display: 'inline'}}>
                          {segment.mode === 'wait' && <i className="fa fa-clock-o" style={{fontSize: "3rem", marginRight: "2rem"}} /> }
                          {segment.mode === 'rideshare' && <i className="fa fa-car" style={{fontSize: "3rem", marginRight: "2rem"}} /> }
                          {segment.mode === 'walk' && <i className="fa fa-female" style={{fontSize: "3rem", marginRight: "2rem"}} /> }
                          {segment.mode === 'transit' && <i className="fa fa-bus" style={{fontSize: "3rem", marginRight: "2rem"}} /> }
                        </li>
                        )}
                      </ul>
                    </div>
                    <div>
                      <span className="lead" style={{marginRight: "2rem"}}>{this.props.route.startTime} - {this.props.route.endTime}</span>
                      <span className="lead" style={{marginRight: "2rem"}}>${this.props.route.cost}</span>
                      <p className="" style={{marginRight: "2rem"}}>{this.props.route.duration}</p>
                    </div>
                  </Col>
                  <Col md="2">
                    <Button block className="btn-1" color="warning" outline type="button" onClick={() => this.toggleModal("defaultModal")}>
                      Details
                    </Button>
                  </Col>
                </Row>
              </CardBody>
            </Card>
          </Row>
        </Container>
        <RouteDetailsModal shouldShow={this.state.defaultModal} toggleModal={() => this.toggleModal("defaultModal")} />
      </>
    );
  }
}

export default RecommendationsListViewItem;
