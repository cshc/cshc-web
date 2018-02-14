import { handleActions } from 'redux-actions';
import dotProp from 'dot-prop-immutable';
import { MatchAward } from 'util/constants';
import {
  SET_MATCH_RESULT,
  ADD_APPEARANCE,
  UPDATE_APPEARANCE,
  REMOVE_APPEARANCE,
  SET_MATCH_REPORT,
  ADD_AWARD_WINNER,
  REMOVE_AWARD_WINNER,
  UPDATE_AWARD_WINNER,
  ADD_PLAYER_OPTION,
} from '../actions/matchEditActions';

export const initialMatchEditState = {
  playerOptions: [],
  result: {
    ourScore: undefined,
    oppScore: undefined,
    ourHtScore: undefined,
    oppHtScore: undefined,
    altOutcome: undefined,
  },
  appearances: [],
  awardWinners: [],
  report: {
    author: undefined,
    title: undefined,
    content: undefined,
  },
};

const newApperance = (memberId, memberName) => ({
  id: memberId,
  name: memberName,
  member: `${memberId}:${memberName}`,
  greenCard: false,
  yellowCard: false,
  redCard: false,
  goals: 0,
});

let nextAwardWinnerId = 0;

const newAwardWinner = () => {
  nextAwardWinnerId += 1;
  return {
    id: `new-${nextAwardWinnerId}`,
    member: undefined,
    awardee: undefined,
    comment: '',
    award: MatchAward.MOM,
  };
};

const removeItem = (array, index) => [...array.slice(0, index), ...array.slice(index + 1)];

const updateArrayItem = (array, item, index) => [
  ...array.slice(0, index),
  item,
  ...array.slice(index + 1),
];

export default handleActions(
  {
    [SET_MATCH_RESULT]: (state, action) => dotProp.set(state, 'result', action.payload.result),
    [SET_MATCH_REPORT]: (state, action) => dotProp.set(state, 'report', action.payload.report),
    [ADD_APPEARANCE]: (state, action) =>
      dotProp.set(state, 'appearances', list => [
        ...list,
        newApperance(action.payload.memberId, action.payload.memberName),
      ]),
    [UPDATE_APPEARANCE]: (state, action) =>
      dotProp.set(state, `appearances.${action.payload.index}`, action.payload.appearance),
    [REMOVE_APPEARANCE]: (state, action) =>
      dotProp.delete(state, `appearances.${action.payload.index}`),
    [ADD_AWARD_WINNER]: state =>
      dotProp.set(state, 'awardWinners', list => [...list, newAwardWinner()]),
    [UPDATE_AWARD_WINNER]: (state, action) =>
      dotProp.set(state, `awardWinners.${action.payload.index}`, action.payload.awardWinner),
    [REMOVE_AWARD_WINNER]: (state, action) =>
      dotProp.delete(state, `awardWinners.${action.payload.index}`),
    [ADD_PLAYER_OPTION]: (state, action) => {
      const newState = dotProp.set(state, 'appearances', list => [
        newApperance(action.payload.memberId, action.payload.memberName),
        ...list,
      ]);
      return dotProp.set(newState, 'playerOptions', list => [
        {
          value: `${action.payload.memberId}:${action.payload.memberName}`,
          label: action.payload.memberName,
        },
        ...list,
      ]);
    },
  },
  initialMatchEditState,
);
