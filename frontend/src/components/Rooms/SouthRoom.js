import React from 'react';
import styled from "styled-components";
import {getBackgroundColor} from "../../helpers/getBackgroundColor";

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
    return (
        <Room
            onClick={() => props.dialogVisible('southroom')}
            style={{ backgroundColor: getBackgroundColor(props.temperature) }}
        >
            <StyledLabel>
                Pokój Południe
            </StyledLabel>
            <StyledLabel>{`Temperatura: ${props.temperature}℃`}</StyledLabel>
        </Room>
    );
};

export default SouthRoom;
