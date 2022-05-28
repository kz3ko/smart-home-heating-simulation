export const LOGIN_START = 'LOGIN_START';
export const LOGIN_SUCCESS = 'LOGIN_SUCCESS';
export const LOGIN_ERROR = 'LOGIN_ERROR';
export const LOGIN_LOGOUT = 'LOGIN_LOGOUT';
export const SET_LOGGED = 'SET_LOGGED';

const initialState = {
    isLoading: false,
    isLogged: false,
    loginData: null,
    loginFailed: null,
};

export const loginReducer = (state = initialState, action) => {
    switch (action.type) {
        case LOGIN_START:
            return {
                ...state,
                isLoading: true,
                isLogged: false,
                loginData: null,
                loginFailed: null,
            };

        case LOGIN_SUCCESS:
            return {
                ...state,
                isLoading: false,
                isLogged: true,
                loginData: action.payload,
                loginFailed: null,
            };

        case LOGIN_ERROR:
            return {
                ...state,
                isLoading: false,
                isLogged: false,
                loginData: null,
                loginFailed: action.payload,
            };
        case LOGIN_LOGOUT:
            return {
                ...state,
                isLoading: false,
                isLogged: false,
                loginData: false,
                loginFailed: null
            };
        case SET_LOGGED:
            return {
                ...state,
                isLoading: false,
                isLogged: action.payload
            }
        default:
            return state;
    }
};