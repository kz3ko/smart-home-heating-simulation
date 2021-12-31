import React, {useState} from 'react';
import styled from "styled-components";
import {getBackgroundColor} from "../../helpers/getBackgroundColor";
import RFIDSensor from "../Molecules/RFIDSensor/RFIDSensor";

const Room = styled.div`
  width: 225px;
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
  position: absolute;
  top: 463px;
  left: 960px;
  flex-direction: column;
  z-index: 1;
  &:hover {
    color: #fff;
  }
`;
const StyledLabel = styled.p`
  font-size: 18px;
  font-weight: bold;
  text-align: center;
`;

const SouthRoom = props => {
    const [peoples, setPeoples] = useState(0);

    return (
        <Room
            onClick={() => props.dialogVisible('southroom')}
            style={{ backgroundColor: getBackgroundColor(props.temperature, props.optimalThreshold, props.coldThreshold, props.warmThreshold, props.hotThreshold) }}
        >
            <StyledLabel>
                Pokój Południe
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

export default SouthRoom;
