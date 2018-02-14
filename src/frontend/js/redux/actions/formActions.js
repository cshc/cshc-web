import { createAction } from 'redux-actions';

export const SAVE_FORM_STATE = 'SAVE_FORM_STATE';

export const saveFormState = createAction(SAVE_FORM_STATE, (dotProp, data) => ({ dotProp, data }));
