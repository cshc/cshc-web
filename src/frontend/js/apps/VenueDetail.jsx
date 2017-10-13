import VenueDetail from 'components/venues/VenueDetail';
import matches, { initialMatchViewState } from 'redux/reducers/matchReducers';
import render from '../ReactRenderer';

const reducers = {
  matches,
};

const initialState = {
  matches: initialMatchViewState,
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
