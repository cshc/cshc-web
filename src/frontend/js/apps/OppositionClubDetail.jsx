/**
 * The OppositionClubDetail app adds asynchronously-loaded content to the Opposition Club 
 * Details page ('/opposition/clubs/<club_slug>').
 * 
 * This includes previous results and upcoming fixtures against this club
 */

import 'util/monitoring';
import OppositionClubDetail from 'components/opposition/OppositionClubDetail';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

render(OppositionClubDetail, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/opposition/OppositionClubDetail', () => {
    const NewOppositionClubDetail = require('../components/opposition/OppositionClubDetail')
      .default;
    render(NewOppositionClubDetail, reducers, initialState);
  });
}
/* eslint-enable global-require */
