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
            style={{ backgroundColor: getBackgroundColor(props.temperature) }}
        >
            <StyledLabel>
                Pokój Południe
            </StyledLabel>
            <RFIDSensor onTouchPlus={() => setPeoples(peoples + 1)} onTouchMinus={() => setPeoples(peoples - 1)} />
            <StyledLabel>{`Temperatura: ${props.temperature.toFixed(2)}℃`}</StyledLabel>
            <StyledLabel>{`Ilość osób: ${props.numberOfPeople}`}</StyledLabel>
        </Room>
    );
};

export default SouthRoom;
