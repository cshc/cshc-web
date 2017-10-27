import { createAction } from 'redux-actions';

/**
 * Action to set the view type for a particular named view.
 */
export const SET_VIEW_TYPE = 'SET_VIEW_TYPE';

export const setViewType = createAction(SET_VIEW_TYPE, (view, viewType) => ({ view, viewType }));
