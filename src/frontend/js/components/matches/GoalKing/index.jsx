import React from 'react';
import PropTypes from 'prop-types';
import GoalKingTable from './GoalKingTable';
import GoalKingFilterSet from './GoalKingFilterSet';

const GoalKingWrapper = ({ season, teams }) => (
  <div>
    <GoalKingFilterSet teams={teams} />
    <GoalKingTable season={season} />
  </div>
);

GoalKingWrapper.propTypes = {
  season: PropTypes.string.isRequired,
  teams: PropTypes.arrayOf(
    PropTypes.shape({
      slug: PropTypes.string,
      long_name: PropTypes.string,
    }),
  ).isRequired,
};

export default GoalKingWrapper;
