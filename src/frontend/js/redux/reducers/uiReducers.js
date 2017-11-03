import { handleActions } from 'redux-actions';

import { ViewType, SwitchableView, FilterName, NoFilter } from 'util/constants';
import { SET_VIEW_TYPE, SET_DATA_FILTER } from '../actions/uiActions';

export const initialViewState = {
  viewTypes: {
    [SwitchableView.MatchList]: ViewType.Table,
    [SwitchableView.SquadRoster]: ViewType.Cards,
    [SwitchableView.VenueList]: ViewType.Map,
    [SwitchableView.MemberList]: ViewType.List,
  },
  activeFilters: {
    [FilterName.Gender]: NoFilter,
    [FilterName.Team]: NoFilter,
    [FilterName.Current]: true,
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
    // Set a value for a particular named filter
    [SET_DATA_FILTER]: (state, action) => ({
      ...state,
      activeFilters: {
        ...state.activeFilters,
        [action.payload.filterName]: action.payload.filterValue,
      },
    }),
  },
  initialViewState,
);
