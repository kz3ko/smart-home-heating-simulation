import React from 'react';
import {ButtonWrapper} from "./Button.styles";

const Button = ({onClick, children, disabled}) => {
    return (
        <ButtonWrapper
            onClick={onClick}
            disabled={disabled}
        >
            {children}
        </ButtonWrapper>
    );
};

export default Button;