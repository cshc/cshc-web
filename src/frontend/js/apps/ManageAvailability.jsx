/**
 * The TeamPlayingAvailability app provides an interface for team captains to 
 * view and manage the availability of players for their team.
 */

import 'util/monitoring';
import ManageAvailability from 'components/availability/ManageAvailability';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

render(ManageAvailability, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/availability/ManageAvailability', () => {
    const NewManageAvailability = require('../components/availability/ManageAvailability').default;
    render(NewManageAvailability, reducers, initialState);
  });
}
/* eslint-enable global-require */
