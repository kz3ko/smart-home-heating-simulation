import React, { useEffect, useState } from 'react';
import { Box, Button, TextField } from '@mui/material';
import { loginFunction } from '../redux/actions/loginActions';
import { connect } from 'react-redux';
import { withRouter } from 'react-router';

const LoginPage = ({ loginReducer, loginFunction, history }) => {
    const [login, setLogin] = useState('karolina');
    const [password, setPassword] = useState('karolina');

    useEffect(() => {
        if(loginReducer.loginFailed){
            setTimeout(() => {
                alert('Błąd logowania');
            }, 500)
        }
    },[])

    return (
        <Box sx={{ display: 'flex', flex: 1, height: '100vh', justifyContent: 'center', alignItems: 'center' }}>
            <Box sx={{ display: 'flex', flexDirection: 'column' }}>
                <img src={'https://images.creativemarket.com/0.1.0/ps/7606092/1820/1214/m1/fpnw/wm0/smart-home-.jpg?1579263722&s=7ad69b47f1cf23b7b71fa66316aeeed0'} style={{ width: 500 }}/>
                <TextField
                    label={'Login'}
                    value={login}
                    onChange={(e) => setLogin(e.target.value)}
                />
                <TextField
                    label={'Hasło'}
                    type={'password'}
                    sx={{ width: 500, mt: 3 }}
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <Button
                    variant={'contained'}
                    sx={{ mt: 3 }}
                    onClick={() => loginFunction(login, password, () => history.push('/home'), () => console.log('Error'))}
                >
                    Log in
                </Button>
            </Box>
        </Box>
    );
};

const mapStateToProps = ({ loginReducer }) => {
    return { loginReducer };
};

const mapDispatchToProps = (dispatch) => {
    return {
        loginFunction: (login, password, successCallback, errorCallback) =>
            dispatch(loginFunction(login, password, successCallback, errorCallback)),
    };
};

export default connect(mapStateToProps, mapDispatchToProps)(withRouter(LoginPage));