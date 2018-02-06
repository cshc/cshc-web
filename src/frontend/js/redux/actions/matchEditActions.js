import { createAction } from 'redux-actions';

export const SET_MATCH_RESULT = 'SET_MATCH_RESULT';
export const ADD_APPEARANCE = 'ADD_APPEARANCE';
export const UPDATE_APPEARANCE = 'UPDATE_APPEARANCE';
export const REMOVE_APPEARANCE = 'REMOVE_APPEARANCE';
export const SET_MATCH_REPORT = 'SET_MATCH_REPORT';
export const ADD_AWARD_WINNER = 'ADD_AWARD_WINNER';
export const UPDATE_AWARD_WINNER = 'UPDATE_AWARD_WINNER';
export const REMOVE_AWARD_WINNER = 'REMOVE_AWARD_WINNER';
export const ADD_PLAYER_OPTION = 'ADD_PLAYER_OPTION';

export const setMatchResult = createAction(SET_MATCH_RESULT, result => ({ result }));

export const addAppearance = createAction(ADD_APPEARANCE, (memberId, memberName) => ({
  memberId,
  memberName,
}));
export const updateAppearance = createAction(UPDATE_APPEARANCE, (index, appearance) => ({
  index,
  appearance,
}));
export const removeAppearance = createAction(REMOVE_APPEARANCE, index => ({
  index,
}));

export const setMatchReport = createAction(SET_MATCH_REPORT, report => ({ report }));

export const addAwardWinner = createAction(ADD_AWARD_WINNER);
export const updateAwardWinner = createAction(UPDATE_AWARD_WINNER, (awardWinner, index) => ({
  awardWinner,
  index,
}));
export const removeAwardWinner = createAction(REMOVE_AWARD_WINNER, index => ({
  index,
}));

export const addPlayerOption = createAction(ADD_PLAYER_OPTION, (memberId, memberName) => ({
  memberId,
  memberName,
}));
