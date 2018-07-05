import React from 'react';
import PropTypes from 'prop-types';
import { default as dateFormat } from 'date-fns/format';
import Match from 'models/match';

const MatchTime = ({ match, format }) => (
  <span>{match.time ? dateFormat(Match.datetime(match), format) : null}</span>
);

MatchTime.propTypes = {
  match: PropTypes.shape({
    date: PropTypes.string.isRequired,
    time: PropTypes.string,
  }).isRequired,
  format: PropTypes.string,
};

MatchTime.defaultProps = {
  format: 'H:mm',
};

export default MatchTime;
