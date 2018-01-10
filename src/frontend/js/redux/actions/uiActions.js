import { createAction } from 'redux-actions';

/**
 * Action to set the view type for a particular named view.
 */
export const SET_VIEW_TYPE = 'SET_VIEW_TYPE';

/**
 * Action to set the value of a named filter.
 * 
 * Filter name must be a string.
 * Filter value can be any type.
 */
export const SET_DATA_FILTER = 'SET_DATA_FILTER';

/**
 * Action to set the current page index of paginated table data
 */
export const SET_PAGE_INDEX = 'SET_PAGE_INDEX';

/**
 * Action to set the page size of paginated table data
 */
export const SET_PAGE_SIZE = 'SET_PAGE_SIZE';

export const setViewType = createAction(SET_VIEW_TYPE, (view, viewType) => ({ view, viewType }));

export const setDataFilter = createAction(SET_DATA_FILTER, (filterName, filterValue) => ({
  filterName,
  filterValue,
}));

export const setPageIndex = createAction(SET_PAGE_INDEX, (tableId, pageInfo, pageIndex) => ({
  tableId,
  pageInfo,
  pageIndex,
}));

export const setPageSize = createAction(
  SET_PAGE_SIZE,
  (tableId, pageInfo, pageSize, pageIndex) => ({
    tableId,
    pageInfo,
    pageSize,
    pageIndex,
  }),
);
