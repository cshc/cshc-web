/**
 * The VenueDetail app adds asynchronously loaded content to the venue details page ('/venues/<venue_slug>')
 * 
 * This includes past and upcoming fixtures at this venue.
 */

import VenueDetail from 'components/venues/VenueDetail';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

render(VenueDetail, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/venues/VenueDetail', () => {
    const NewVenueDetail = require('../components/venues/VenueDetail').default;
    render(NewVenueDetail, reducers, initialState);
  });
}
/* eslint-enable global-require */
