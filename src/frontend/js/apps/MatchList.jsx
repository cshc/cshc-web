/**
 * The MatchList app provides a filterable/searchable list of matches
 */

import 'util/monitoring';
import MatchList from 'components/matches/MatchList';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

render(MatchList, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/matches/MatchList', () => {
    const NewMatchList = require('../components/matches/MatchList').default;
    render(NewMatchList, reducers, initialState);
  });
}
/* eslint-enable global-require */
