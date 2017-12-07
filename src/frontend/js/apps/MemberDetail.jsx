/**
 * The MemberDetail app adds asynchronously loaded content to the member details page ('/members/<member_id>')
 * 
 * This includes playing record and club involvement details.
 */

import 'util/monitoring';
import Urls from 'util/urls';
import MemberDetail from 'components/members/MemberDetail';
import ui, { initialViewState } from 'redux/reducers/uiReducers';
import render from '../ReactRenderer';

const reducers = {
  ui,
};

const initialState = {
  ui: initialViewState,
};

const baseUrl = Urls.member_detail(window.props.member.id);

render(MemberDetail, reducers, initialState, baseUrl);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/members/MemberDetail', () => {
    const NewMemberDetail = require('../components/members/MemberDetail').default;
    render(NewMemberDetail, reducers, initialState, baseUrl);
  });
}
/* eslint-enable global-require */
