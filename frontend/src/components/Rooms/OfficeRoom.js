import React, {useState} from 'react';
import styled from "styled-components";
import {getBackgroundColor} from "../../helpers/getBackgroundColor";
import RFIDSensor from "../Molecules/RFIDSensor/RFIDSensor";

const OfficeRoom = props => {
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

      &:hover {
        color: #fff;
      }
    `;
    const StyledLabel = styled.p`
      font-size: 18px;
      font-weight: bold;
      text-align: center;
    `;

    return (
        <Room
            onClick={() => props.dialogVisible('officeroom')}
            style={{ backgroundColor: getBackgroundColor(props.temperature) }}
        >
            <StyledLabel>
                Biuro
            </StyledLabel>
            <RFIDSensor onTouchPlus={() => setPeoples(peoples + 1)} onTouchMinus={() => setPeoples(peoples - 1)} />
            <StyledLabel>{`Temperatura: ${props.temperature.toFixed(2)}℃`}</StyledLabel>
            <StyledLabel>{`Ilość osób: ${props.numberOfPeople}`}</StyledLabel>
        </Room>
    );
};

export default OfficeRoom;
