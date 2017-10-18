import { handleActions } from 'redux-actions';
import { getCookie, setCookie } from 'util/cookies';

import { ViewType, SwitchableView } from 'util/constants';
import { SET_VIEW_TYPE } from '../actions/uiActions';

const ViewTypeCookiePrefix = 'cshc-view-type-';

export const initialViewState = {
  viewTypes: {
    [SwitchableView.MatchList]: getCookie(
      ViewTypeCookiePrefix + SwitchableView.MatchList,
      ViewType.Table,
    ),
    [SwitchableView.SquadRoster]: getCookie(
      ViewTypeCookiePrefix + SwitchableView.SquadRoster,
      ViewType.Cards,
    ),
  },
};

export default handleActions(
  {
    [SET_VIEW_TYPE]: (state, action) => {
      setCookie(ViewTypeCookiePrefix + action.payload.view, action.payload.viewType);
      return {
        ...state,
        viewTypes: {
          ...state.viewTypes,
          [action.payload.view]: action.payload.viewType,
        },
      };
    },
  },
  initialViewState,
);
