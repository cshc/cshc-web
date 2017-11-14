/**
 * The TeamDetail app adds asynchronously-loaded content to the Team Details 
 * page ('/teams/<team_slug>').
 * 
 * This also applies to the team details page for previous seasons 
 * ('/teams/<team_slug>/<season_slug>')
 * 
 * This includes Results, Fixtures, the League Table and the Squad Roster.
 */

import TeamDetail from 'components/teams/TeamDetail';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import { FilterName, NoFilter } from 'util/constants';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

// Set the FixtureType filter to the 'All' option
const initialState = {
  ui: {
    ...initialViewState,
    activeFilters: {
      ...initialViewState.activeFilters,
      [FilterName.FixtureType]: NoFilter,
    },
  },
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
