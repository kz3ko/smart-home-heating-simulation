import React from 'react';
import styled from "styled-components";
import {getBackgroundColor} from "../../helpers/getBackgroundColor";

const NorthRoom = props => {
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
            onClick={() => props.dialogVisible('northroom')}
            style={{ backgroundColor: getBackgroundColor(props.temperature) }}
        >
            <StyledLabel>
                Pokój Północ
            </StyledLabel>
            <StyledLabel>{`Temperatura: ${props.temperature}℃`}</StyledLabel>
        </Room>
    );
};

export default NorthRoom;
