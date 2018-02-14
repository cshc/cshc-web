import { handleActions } from 'redux-actions';
import dotProp from 'dot-prop-immutable';
import { SAVE_FORM_STATE } from '../actions/formActions';

export const initialFormState = {};

export default handleActions(
  {
    [SAVE_FORM_STATE]: (state, action) =>
      dotProp.set(state, action.payload.dotProp, action.payload.data),
  },
  initialFormState,
);
