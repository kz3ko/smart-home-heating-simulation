import React, {useState} from 'react';
import styled from 'styled-components';
import {getBackgroundColor} from "../../helpers/getBackgroundColor";
import RFIDSensor from "../Molecules/RFIDSensor/RFIDSensor";

const RoomComponent = props => {

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

      &:hover {
        color: #fff;
      }
    `;
    const StyledLabel = styled.p`
      font-size: 16px;
      font-weight: bold;
    `;

    return (
        <Room
            onClick={() => props.selectRoom(props.roomId)}
            style={{
                backgroundColor: getBackgroundColor(props.temperature, props.optimalThreshold, props.coldThreshold, props.warmThreshold, props.hotThreshold, props.coolDownTemp, props.numberOfPeople)
            }}
        >
            <StyledLabel>
                {props.title}
            </StyledLabel>
            <RFIDSensor
                onTouchPlus={() => props.setPeopleAmount(props.roomId, props.numberOfPeople + 1)}
                onTouchMinus={() => {
                    if (props.numberOfPeople - 1 >= 0) {
                        props.setPeopleAmount(props.roomId, props.numberOfPeople - 1)
                    } else {
                        alert('Pokój jest już pusty.')
                    }
                }}
            />
            <StyledLabel>{`Temperatura: ${props.temperature.toFixed(2)}℃`}</StyledLabel>
            <StyledLabel>{`Ilość osób: ${props.numberOfPeople}`}</StyledLabel>
        </Room>
    );
};

export default RoomComponent;
