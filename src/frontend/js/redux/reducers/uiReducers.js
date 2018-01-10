import { handleActions } from 'redux-actions';
import { DefaultPageQueryProps } from 'components/common/PropTypes';

import { ViewType, SwitchableView, FilterName, NoFilter } from 'util/constants';
import {
  SET_VIEW_TYPE,
  SET_DATA_FILTER,
  SET_PAGE_INDEX,
  SET_PAGE_SIZE,
} from '../actions/uiActions';

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
  pageQueries: {},
};

const updatePageIndex = (payload, pageQuery = DefaultPageQueryProps) => {
  console.log(payload);
  return {
    ...pageQuery,
    pageIndex: payload.pageIndex,
    after: payload.pageIndex > pageQuery.pageIndex ? payload.pageInfo.endCursor : undefined,
    before: payload.pageIndex < pageQuery.pageIndex ? payload.pageInfo.startCursor : undefined,
  };
};

const updatePageSize = (payload, pageQuery = DefaultPageQueryProps) => {
  console.log(payload);
  return {
    ...pageQuery,
    pageIndex: payload.pageIndex,
    first: payload.pageSize,
    after: payload.pageIndex > pageQuery.pageIndex ? payload.pageInfo.endCursor : undefined,
    before: payload.pageIndex < pageQuery.pageIndex ? payload.pageInfo.startCursor : undefined,
  };
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
    [SET_PAGE_INDEX]: (state, action) => ({
      ...state,
      pageQueries: {
        ...state.pageQueries,
        [action.payload.tableId]: updatePageIndex(
          action.payload,
          state.pageQueries[action.payload.tableId],
        ),
      },
    }),
    [SET_PAGE_SIZE]: (state, action) => ({
      ...state,
      pageQueries: {
        ...state.pageQueries,
        [action.payload.tableId]: updatePageSize(
          action.payload,
          state.pageQueries[action.payload.tableId],
        ),
      },
    }),
  },
  initialViewState,
);
