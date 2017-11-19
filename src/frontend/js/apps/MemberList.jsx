/**
 * The MemberList app provides a filterable/searchable list of members with both map
 * and list views
 */

import 'util/monitoring';
import MemberList from 'components/members/MemberList';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

render(MemberList, reducers, initialState);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/members/MemberList', () => {
    const NewMemberList = require('../components/members/MemberList').default;
    render(NewMemberList, reducers, initialState);
  });
}
/* eslint-enable global-require */
