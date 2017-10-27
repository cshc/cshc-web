import { handleActions } from 'redux-actions';

import { ViewType, SwitchableView } from 'util/constants';
import { SET_VIEW_TYPE } from '../actions/uiActions';

export const initialViewState = {
  viewTypes: {
    [SwitchableView.MatchList]: ViewType.Table,
    [SwitchableView.SquadRoster]: ViewType.Cards,
  },
};

export default handleActions(
  {
    // Set the view type for the named view.
    [SET_VIEW_TYPE]: (state, action) => ({
      ...state,
      viewTypes: {
        ...state.viewTypes,
        [action.payload.view]: action.payload.viewType,
      },
    }),
  },
  initialViewState,
);
