import TeamDetail from 'components/teams/TeamDetail';
import matches, { initialMatchViewState } from 'redux/reducers/matchReducers';
import render from '../ReactRenderer';

const reducers = {
  matches,
};

const initialState = {
  matches: initialMatchViewState,
};

render(TeamDetail, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/teams/TeamDetail', () => {
    const NewTeamDetail = require('../components/teams/TeamDetail').default;
    render(NewTeamDetail, reducers, initialState);
  });
}
/* eslint-enable global-require */
