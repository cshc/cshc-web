import { handleActions } from 'redux-actions';
import { MatchAward } from 'util/constants';
import Match from 'models/match';
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
  dirty: false,
  playerOptions: [],
  result: {
    errors: [],
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
    [SET_MATCH_RESULT]: (state, action) => ({
      ...state,
      dirty: true,
      result: {
        ...action.payload.result,
        errors: Match.resultErrors(action.payload.result),
      },
    }),
    [SET_MATCH_REPORT]: (state, action) => ({
      ...state,
      dirty: true,
      report: action.payload.report,
    }),
    [ADD_APPEARANCE]: (state, action) => ({
      ...state,
      dirty: true,
      appearances: [
        newApperance(action.payload.memberId, action.payload.memberName),
        ...state.appearances.slice(0),
      ],
    }),
    [UPDATE_APPEARANCE]: (state, action) => ({
      ...state,
      dirty: true,
      appearances: updateArrayItem(
        state.appearances,
        action.payload.appearance,
        action.payload.index,
      ),
    }),
    [REMOVE_APPEARANCE]: (state, action) => ({
      ...state,
      dirty: true,
      appearances: removeItem(state.appearances, action.payload.index),
    }),
    [ADD_AWARD_WINNER]: state => ({
      ...state,
      dirty: true,
      awardWinners: state.awardWinners.concat(newAwardWinner()),
    }),
    [UPDATE_AWARD_WINNER]: (state, action) => ({
      ...state,
      dirty: true,
      awardWinners: updateArrayItem(
        state.awardWinners,
        action.payload.awardWinner,
        action.payload.index,
      ),
    }),
    [REMOVE_AWARD_WINNER]: (state, action) => ({
      ...state,
      dirty: true,
      awardWinners: removeItem(state.awardWinners, action.payload.index),
    }),
    [ADD_PLAYER_OPTION]: (state, action) => ({
      ...state,
      dirty: true,
      appearances: [
        newApperance(action.payload.memberId, action.payload.memberName),
        ...state.appearances.slice(0),
      ],
      playerOptions: [
        {
          value: `${action.payload.memberId}:${action.payload.memberName}`,
          label: action.payload.memberName,
        },
        ...state.playerOptions.slice(0),
      ],
    }),
  },
  initialMatchEditState,
);
