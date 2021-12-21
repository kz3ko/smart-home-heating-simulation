import React from 'react';
import styled from 'styled-components';
import rfidLogo from '../../../assets/rfid-logo.png';

const StyledSensor = styled.div`
  display: flex;
  width: 80px;
  height: 40px;
  background-color: white;
  border-radius: 10px;
  align-items: center;
  justify-content: center;
  flex-direction: row;
`;

const SensorImage = styled.img`
  display: flex;
  width: 30px;
  height: 30px;
`;

const Button = styled.button`
  width: 16px;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-left: 6px;
  margin-right: 6px;
`;

const RFIDSensor = props => {
    return (
        <StyledSensor onClick={e => e.stopPropagation()}>
            <Button onClick={() => props.onTouchMinus()}>-</Button>
            <SensorImage src={rfidLogo} />
            <Button onClick={() => props.onTouchPlus()}>+</Button>
        </StyledSensor>
    );
};

export default RFIDSensor;
