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
import React, { Component } from 'react';
// nodejs library that concatenates classes
import classnames from 'classnames';

// reactstrap components
import { Card, CardBody, NavItem, NavLink, Nav, TabContent, TabPane, Row, Col } from 'reactstrap';

class TripInputTabs extends Component {
    state = {
        iconTabs: 1, // 1 - time, 2 - price
        // plainTabs: 1,
    };

    toggleNavs = (e, optimiseFor) => {
        e.preventDefault();

        this.props.onToggle(optimiseFor);

        // this.setState({
        //     [state]: index,
        // });
    };

    render() {
        return (
            <Row className="justify-content-center">
                <Col lg="12">
                    <div className="mb-3">
                        <small className="text-uppercase font-weight-bold">What's more important to you?</small>
                    </div>
                    <div className="nav-wrapper">
                        <Nav className="nav-fill flex-column flex-md-row" id="tabs-icons-text" pills role="tablist">
                            <NavItem>
                                <NavLink
                                    aria-selected={this.props.optimiseFor === 'time'}
                                    className={classnames('mb-sm-3 mb-md-0', {
                                        active: this.props.optimiseFor === 'time',
                                    })}
                                    onClick={e => this.toggleNavs(e, 'time')}
                                    href="#"
                                    role="tab"
                                >
                                    <i className="ni ni-time-alarm mr-2" />
                                    Time
                                </NavLink>
                            </NavItem>
                            <NavItem>
                                <NavLink
                                    aria-selected={this.props.optimiseFor === 'price'}
                                    className={classnames('mb-sm-3 mb-md-0', {
                                        active: this.props.optimiseFor === 'price',
                                    })}
                                    onClick={e => this.toggleNavs(e, 'price')}
                                    href="#"
                                    role="tab"
                                >
                                    <i className="ni ni-money-coins mr-2" />
                                    Price
                                </NavLink>
                            </NavItem>
                        </Nav>
                    </div>
                    <Card className="shadow">
                        <CardBody>
                            <TabContent activeTab={this.props.optimiseFor}>
                                <TabPane tabId="time">
                                    <p className="description">
                                        Choose this option if you want us to optimize for time. This may mean that your
                                        costs may be slightly higher.
                                    </p>
                                </TabPane>
                                <TabPane tabId="price">
                                    <p className="description">
                                        Choose this option if you want us to optimize for cost. This may mean that it
                                        takes slightly longer to get to your destination.
                                    </p>
                                </TabPane>
                            </TabContent>
                        </CardBody>
                    </Card>
                </Col>
            </Row>
        );
    }
}

export default TripInputTabs;
