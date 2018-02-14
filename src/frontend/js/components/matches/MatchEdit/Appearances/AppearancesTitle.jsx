import React from 'react';
import { connect } from 'react-redux';
import Match from 'models/match';

const mapStateToText = state => ({
  text: `Players${state.matchState.appearances.length && Match.wasPlayed(state.matchState.result)
    ? ` (${state.matchState.appearances.length})`
    : ''}`,
});

/**
 * A dynamic title for the Players slide, including a count of the 
 * number of players selected.
 */
export default connect(mapStateToText)(({ text }) => <span>{text}</span>);
