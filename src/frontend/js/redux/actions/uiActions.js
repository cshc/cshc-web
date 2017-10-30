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

export const setViewType = createAction(SET_VIEW_TYPE, (view, viewType) => ({ view, viewType }));

export const setDataFilter = createAction(SET_DATA_FILTER, (filterName, filterValue) => ({
  filterName,
  filterValue,
}));
