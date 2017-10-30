/**
 * The VenueList app provides a filterable/searchable list of venues with both map
 * and list views
 */

import VenueList from 'components/venues/VenueList';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

render(VenueList, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/venues/VenueList', () => {
    const NewVenueList = require('../components/venues/VenueList').default;
    render(NewVenueList, reducers, initialState);
  });
}
/* eslint-enable global-require */
