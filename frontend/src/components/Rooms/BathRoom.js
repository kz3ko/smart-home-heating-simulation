import React, {useState} from 'react';
import styled from "styled-components";
import {getBackgroundColor} from "../../helpers/getBackgroundColor";
import RFIDSensor from "../Molecules/RFIDSensor/RFIDSensor";

const BathRoom = props => {
    const [peoples, setPeoples] = useState(0);

    const Room = styled.div`
      width: ${props.width}px;
      height: ${props.height}px;
      top: ${props.yPos}px;
      left: ${props.xPos}px;
      display: flex;
      align-items: center;
      justify-content: center;
      position: absolute;
      flex-direction: column;
      z-index: 2;

      &:hover {
        color: #fff;
      }
    `;
    const StyledLabel = styled.p`
      font-size: 16px;
      font-weight: bold;
      text-align: center;
    `;
    return (
        <Room
            onClick={() => props.dialogVisible('bathroom')}
            style={{ backgroundColor: getBackgroundColor(props.temperature) }}
        >
            <StyledLabel>
                Łazienka
            </StyledLabel>
            <RFIDSensor onTouchPlus={() => setPeoples(peoples + 1)} onTouchMinus={() => setPeoples(peoples - 1)} />
            <StyledLabel>{`Temperatura: ${props.temperature.toFixed(2)}℃`}</StyledLabel>
            <StyledLabel>{`Ilość osób: ${props.numberOfPeople}`}</StyledLabel>
        </Room>
    );
};

export default BathRoom;
