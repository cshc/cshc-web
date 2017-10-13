import { createAction } from 'redux-actions';

export const SET_MATCH_VIEW_TYPE = 'SET_MATCH_VIEW_TYPE';

export const setMatchViewType = createAction(SET_MATCH_VIEW_TYPE, style => style);
