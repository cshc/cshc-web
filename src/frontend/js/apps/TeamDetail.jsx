import TeamDetail from 'components/teams/TeamDetail';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
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
