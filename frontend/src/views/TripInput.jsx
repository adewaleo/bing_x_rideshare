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
// import classnames from "classnames";

// reactstrap components
import { FormGroup, Container, Row, Button, Form, Label } from 'reactstrap';
import axios from 'axios';
import { geolocated } from 'react-geolocated';
import GooglePlacesAutocomplete from 'react-google-places-autocomplete';

import TripInputTabs from './TripInputTabs.jsx';

class TripInput extends Component {
    state = {
        start: null,
        destination: null,
        optimiseFor: 'time',
    };

    handleToggle = optimiseFor => {
        this.setState({ optimiseFor });
    };

    // placeSearch = async query => {
    //     try {
    //         const response = await axios.get(`http://127.0.0.1:5000/place_autocomplete/'${query}`);
    //         console.log(response);
    //     } catch (error) {
    //         console.error(error);
    //     }
    // };

    handleSubmit = async () => {
        const { start, destination, optimiseFor } = this.state;
        try {
            const startResponse = await axios.get(`http://127.0.0.1:5000/place_autocomplete/'${start}`);
            const destResponse = await axios.get(`http://127.0.0.1:5000/place_autocomplete/'${destination}`);

            const { lat: startLat, long: startLong } = startResponse.data[0];
            const { lat: destLat, long: destLong } = destResponse.data[0];

            const response = await axios.post('http://127.0.0.1:5000/recommendations', {
                dest: { lat: destLat, long: destLong },
                start: { lat: startLat, long: startLong },
                optimse_for: optimiseFor,
            });

            console.log(response);
        } catch (error) {
            console.error(error);
        }

        // try {
        //     const response = await axios.post('http://127.0.0.1:5000/recommendations', {
        //         dest: { lat: 11.3, long: -12222.5 },
        //         start: { lat: 11.3, long: -12222.5 },
        //         optimse_for: 'cost',
        //     });
        //     // const response = await axios.get(`http://127.0.0.1:5000/test`);
        //     console.log(response);
        // } catch (error) {
        //     console.error(error);
        // }
    };

    render() {
        const { props, optimiseFor } = this;

        return (
            <>
                <Container>
                    <Row className="py-3 align-items-center">
                        <h3 className="heading-title mb-0">Enter your trip</h3>
                    </Row>
                    <Form>
                        <FormGroup>
                            <Label for="start">Start</Label>
                            {/* <Input type="text" name="start" id="start" placeholder="Start" /> */}
                            <div>
                                <GooglePlacesAutocomplete
                                    onSelect={({ description }) => this.setState({ start: description })}
                                    placeholder="Starting point"
                                />
                            </div>
                        </FormGroup>
                        <FormGroup>
                            <Label for="destination">Destination</Label>
                            {/* <Input type="text" name="destination" id="destination" placeholder="Destination" /> */}
                            <div>
                                <GooglePlacesAutocomplete
                                    onSelect={({ description }) => this.setState({ destination: description })}
                                    placeholder="Destination"
                                />
                            </div>
                        </FormGroup>
                        <Row className="py-3 align-items-center" style={{ display: 'grid' }}>
                            <TripInputTabs onToggle={this.handleToggle} optimiseFor={optimiseFor} />
                        </Row>
                        <Button color="primary" block onClick={this.handleSubmit}>
                            Submit
                        </Button>
                    </Form>
                    {/* <Row className="py-3 align-items-center">
                                                <FormGroup>
                                                        <Input placeholder="Start" type="text" />
                                                </FormGroup>
                                        </Row>
                                        <Row className="py-3 align-items-center">
                                                <FormGroup>
                                                        <Input placeholder="Destination" type="text" />
                                                </FormGroup>
                                        </Row>
                                        */}

                    {/* <Button
                                                className="ml-1 btn-neutral btn-icon-only btn-round"
                                                color="success"
                                                href="/recommendations"
                                                size="lg"
                                        >
                                                Go
                                        </Button> */}
                </Container>
            </>
        );
    }
}

export default geolocated({
    positionOptions: {
        enableHighAccuracy: true,
    },
    userDecisionTimeout: 5000,
})(TripInput);
