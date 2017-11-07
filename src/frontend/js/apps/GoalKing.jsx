/**
 * The GoalKing app provides a filterable/searchable list of Goal King entries.
 */

import GoalKing from 'components/matches/GoalKing';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import { FilterName, Gender } from 'util/constants';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

// Set the Season filter to the current season and
// the gender options to both men and ladies
const initialState = {
  ui: {
    ...initialViewState,
    activeFilters: {
      ...initialViewState.activeFilters,
      [FilterName.Season]: window.props.current_season,
      [FilterName.GoalKingGender]: [Gender.Male, Gender.Female],
    },
  },
};

render(GoalKing, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/matches/GoalKing', () => {
    const NewGoalKing = require('../components/matches/GoalKing').default;
    render(NewGoalKing, reducers, initialState);
  });
}
/* eslint-enable global-require */
