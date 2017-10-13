import { handleActions } from 'redux-actions';
import { getCookie, setCookie } from 'util/cookies';

import { ViewType } from 'components/matches/MatchList/MatchList';
import { SET_MATCH_VIEW_TYPE } from '../actions/matchActions';

const ViewTypeCookie = 'cshc-match-view-type';

export const initialMatchViewState = {
  viewType: getCookie(ViewTypeCookie, ViewType.grid),
  isExpanded: false,
};

export default handleActions(
  {
    [SET_MATCH_VIEW_TYPE]: (state, action) => {
      setCookie(ViewTypeCookie, action.payload);
      return {
        ...state,
        viewType: action.payload,
      };
    },
  },
  initialMatchViewState,
);
