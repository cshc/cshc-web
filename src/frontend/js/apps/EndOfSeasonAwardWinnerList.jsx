/**
 * The EndOfSeasonAwardWinnerList app provides a filterable list of End of Season
 * award winners.
 */

import 'util/monitoring';
import EndOfSeasonAwardWinnerList from 'components/awards/EndOfSeasonAwardWinnerList';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

render(EndOfSeasonAwardWinnerList, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/awards/EndOfSeasonAwardWinnerList', () => {
    const NewEndOfSeasonAwardWinnerList = require('../components/awards/EndOfSeasonAwardWinnerList')
      .default;
    render(NewEndOfSeasonAwardWinnerList, reducers, initialState);
  });
}
/* eslint-enable global-require */
