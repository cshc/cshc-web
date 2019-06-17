/**
 * The GoalKing app provides a filterable/searchable list of Goal King entries.
 */
import 'util/monitoring';
import OppositionClubList from 'components/opposition/OppositionClubList';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

render(OppositionClubList, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/opposition/OppositionClubList', () => {
    const NewOppositionClubList = require('../components/opposition/OppositionClubList').default;
    render(NewOppositionClubList, reducers, initialState);
  });
}
/* eslint-enable global-require */
