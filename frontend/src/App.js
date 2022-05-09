import HouseScene from "./components/HouseScene/HouseScene";
import LoginPage from './pages/LoginPage';
import { Route, Switch, withRouter } from 'react-router-dom';
import { connect } from 'react-redux';
import LoadingSpinner from './components/Atoms/Spinner/Spinner';

function App({ loginReducer }) {

  return (
      <Switch>
          {loginReducer.isLoading ? (
              <LoadingSpinner />
          ) : (
              <>
                  {loginReducer.isLogged ? (
                      <>
                          <Route exact path={'/main'} component={HouseScene}/>
                      </>
                  ) : (
                      <>
                          <Route exact path={'/'} component={LoginPage}/>
                      </>
                  )}
              </>
          )}
      </Switch>
  );
}

const mapStateToProps = ({loginReducer}) => {
    return {loginReducer};
};

const AppWithRouter = withRouter(App);

export default connect(mapStateToProps)(AppWithRouter);