/**
 * The MatchDetail app adds asynchronously loaded content to the match details page ('/match/<match_id>')
 * 
 * This includes the fixture history between two teams.
 */

import 'util/monitoring';
import Urls from 'util/urls';
import MatchDetail from 'components/matches/MatchDetail';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

const baseUrl = Urls.match_detail(window.props.matchId);

render(MatchDetail, reducers, initialState, baseUrl);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/matches/MatchDetail', () => {
    const NewMatchDetail = require('../components/matches/MatchDetail').default;
    render(NewMatchDetail, reducers, initialState, baseUrl);
  });
}
/* eslint-enable global-require */
