import styled, {css} from 'styled-components';

const ButtonWrapper = styled.button`
    width: 75%;
    height: 30px;
    border-radius: 10px;
    border-width: 0px;
    text-align: center;
    background-color: #f5f5f5;
    font-size: 1.1rem;
    font-family: Montserrat,serif;
    font-weight: 500;
    letter-spacing: 2px;
    @media (max-width: 1200px) {
      font-size: 0.8rem;
    }
    &:hover {
    ${({disabled}) =>
    !disabled &&
    css`
    background-color: #62C370;
    color: #fff;
    `
}
    }
    ${({disabled}) =>
    disabled &&
    css`
      opacity: 70%;
    `}
`;

const StyledButtonText = styled.p`
  font-size: 15px;
  font-family: Montserrat,serif;
  @media(max-width: 768px) {
    font-size: 10px;
  }
`;
export {ButtonWrapper};