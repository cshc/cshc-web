/**
 * The GoalKing app provides a filterable/searchable list of Goal King entries.
 */
import 'util/monitoring';
import GoalKing from 'components/matches/GoalKing';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
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
