import React from 'react';
import style from 'styled-components';
import { BeatLoader } from 'react-spinners'

const SpinnerWrapper = style.div`
    display: flex;
    align-items: center;
    justify-content: center;
    margin-top: 25%;
    width: 100%;
    height: 100%;
`;

const LoadingSpinner = () => {
    return(
        <SpinnerWrapper>
            <BeatLoader size={20} color={'#0000FF'}/>
        </SpinnerWrapper>
    );
};

export default LoadingSpinner;