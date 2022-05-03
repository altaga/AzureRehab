import React, { Component } from "react";
import Webcam from "react-webcam";
import './App.css';
import {
    Card, CardHeader, Button, CardBody, CardText, Row, Col
} from 'reactstrap';
import { isMobile } from 'react-device-detect';
import image from './img'

var unirest = require('unirest');

class Cam extends Component {
    constructor(props) {
        super(props);
        this.state = {
            delay: 0,
            value: image,
            dis: false,
        };
        this.webcamRef = React.createRef();
        this.capture = this.capture.bind(this);
    }

    capture() {
        this.setState({
            dis: true
        }, () => {
            const counterDown = setInterval(() => {
                this.setState({ delay: this.state.delay - 1 })
            }, 1000);
            setTimeout(() => {
                clearInterval(counterDown)
                let imageSrc = this.webcamRef.current.getScreenshot();
                unirest('post', 'https://azuretf.azurewebsites.net/api/Azure-TFlite?code=waug9kwZ3VLkid0bBfAprjDmaFril53fL0KKyHAUhV6etLOPLvhUJg==')
                    .send(imageSrc.replace('data:image/jpeg;base64,', ''))
                    .end((res) => {
                        this.setState({
                            value: res.body,
                            dis: false,
                            delay: 0
                        })
                    });
            }, this.state.delay * 1000);
        })
    }


    componentDidMount() {

    }

    render() {
        if (isMobile) {
            document.body.style.backgroundColor = '#17a2b8';
            return (
                <div className="hCentered">
                    <div>
                        <Webcam
                            style={{ borderRadius: "10px" }}
                            audio={false}
                            height={"auto"}
                            ref={this.webcamRef}
                            screenshotFormat="image/jpeg"
                            width="90%"
                        />
                    </div>
                    <div>
                        <Row md="2">
                            <Col style={{ width: "40vw" }}>
                                <Button color="warning" disabled={this.state.dis} style={{ fontSize: "1.5rem", width: "90%" }} size="lg" onClick={this.capture}>Capture</Button>
                            </Col>
                            <Col>
                                <Button color="warning" disabled={this.state.dis} style={{ fontSize: "1.5rem", width: "90%" }} size="lg" onClick={() => {
                                    if (this.state.delay === 0) {
                                        this.setState({
                                            delay: 2
                                        })
                                    }
                                    else if (this.state.delay === 2) {
                                        this.setState({
                                            delay: 5
                                        })
                                    }
                                    else if (this.state.delay === 5) {
                                        this.setState({
                                            delay: 10
                                        })
                                    }
                                    else if (this.state.delay === 10) {
                                        this.setState({
                                            delay: 0
                                        })
                                    }
                                }}>Delay {this.state.delay}</Button>
                            </Col>
                        </Row>
                    </div>
                    <Row md={1}>
                        <Col xs="12">
                        </Col>
                        <Col xs="12">
                            <Card color="info" style={{ height: "100%" }}>
                                <CardHeader className="d-flex justify-content-center">
                                    <div >
                                        <img width={"100%"} src={`data:image/jpg;base64,${this.state.value}`} alt="result" />
                                    </div>
                                </CardHeader>
                                <CardBody className="d-flex justify-content-center">
                                    <CardText style={{ fontSize: "1.5rem" }}>
                                        Result
                                    </CardText>
                                </CardBody>
                            </Card>
                        </Col>
                    </Row>
                </div>
            );
        }
        else {
            return (
                <div style={{
                    margin: "10px",
                }}>
                    <div style={{
                        margin: "10px",
                        fontSize: "2rem",
                        fontWeight: "bold",
                        textAlign: "center"
                    }}>
                        Welcome to the Azure Rehab Demo
                    </div>
                    <Row md="2" style={{ height: "100%" }}>
                        <Col>
                            <Card color="info" style={{ height: "100%" }}>
                                <CardHeader className="d-flex justify-content-center">
                                    <div >
                                        <Webcam
                                            style={{ borderRadius: "10px" }}
                                            audio={false}
                                            height={480}
                                            ref={this.webcamRef}
                                            screenshotFormat="image/jpeg"
                                            width={640}
                                        />
                                    </div>
                                </CardHeader>
                                <CardBody className="d-flex justify-content-center">
                                    <Row md="2">
                                        <Col style={{ width: "40vw" }}>
                                            <Button color="warning" disabled={this.state.dis} style={{ fontSize: "1.5rem", width: "100%" }} size="lg" onClick={this.capture}>Capture</Button>
                                        </Col>
                                        <Col>
                                            <Button color="warning" disabled={this.state.dis} style={{ fontSize: "1.5rem", width: "100%" }} size="lg" onClick={() => {
                                                if (this.state.delay === 0) {
                                                    this.setState({
                                                        delay: 2
                                                    })
                                                }
                                                else if (this.state.delay === 2) {
                                                    this.setState({
                                                        delay: 5
                                                    })
                                                }
                                                else if (this.state.delay === 5) {
                                                    this.setState({
                                                        delay: 10
                                                    })
                                                }
                                                else if (this.state.delay === 10) {
                                                    this.setState({
                                                        delay: 0
                                                    })
                                                }
                                            }}>Delay {this.state.delay}</Button>
                                        </Col>
                                    </Row>
                                </CardBody>
                            </Card>
                        </Col>
                        <Col>
                            <Card color="info" style={{ height: "100%" }}>
                                <CardHeader className="d-flex justify-content-center">
                                    <div >
                                        <img src={`data:image/jpg;base64,${this.state.value}`} alt="result" />
                                    </div>
                                </CardHeader>
                                <CardBody className="d-flex justify-content-center">
                                    <CardText style={{ fontSize: "1.5rem" }}>
                                        Result
                                    </CardText>
                                </CardBody>
                            </Card>
                        </Col>
                    </Row>
                </div>
            );
        }
    }
}

export default Cam;