/**
 * The MatchEdit app adds asynchronously loaded content to the match edit page ('/match/<match_id>/edit')
 * 
 * The React app actually constitutes the whole page content, allowing the relevant person to easily 
 * edit the match details.
 */

import 'util/monitoring';
import Urls from 'util/urls';
import MatchEdit from 'components/matches/MatchEdit';
import { toSelectOption } from 'components/matches/MatchEdit/util';
import matchState from 'redux/reducers/matchEditReducers';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import form from 'redux/reducers/formReducers';
import Appearance from 'models/appearance';
import render from '../ReactRenderer';

const reducers = {
  ui,
  matchState,
  form,
};

const initialMatchState = {
  ...window.props.matchState,
  // Player options, encoded as {id}:{name} are mapped to value ({id}:{name})/label ({name}) pairs
  playerOptions: window.props.matchState.playerOptions.map(toSelectOption),
  // Appearances are mapped to objects with greenCard, yellowCard, redCard boolean fields
  appearances: Appearance.initAppearances(window.props.matchState.appearances),
};

const initialState = {
  ui: initialViewState,
  matchState: initialMatchState,
  form: { matchState: { ...initialMatchState } },
};

const baseUrl = Urls.match_detail(window.props.matchId);

render(MatchEdit, reducers, initialState, baseUrl);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/matches/MatchEdit', () => {
    const NewMatchEdit = require('../components/matches/MatchEdit').default;
    render(NewMatchEdit, reducers, initialState, baseUrl);
  });
}
/* eslint-enable global-require */
