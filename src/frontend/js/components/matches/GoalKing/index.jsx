import React from 'react';
import PropTypes from 'prop-types';
import GoalKingTable from './GoalKingTable';
import GoalKingFilterSet from './GoalKingFilterSet';

const GoalKingWrapper = ({ current_season, seasons, teams }) => (
  <div>
    <GoalKingFilterSet currentSeason={current_season} seasons={seasons} teams={teams} />
    <GoalKingTable currentSeason={current_season} />
  </div>
);

GoalKingWrapper.propTypes = {
  current_season: PropTypes.string.isRequired,
  seasons: PropTypes.arrayOf(PropTypes.string).isRequired,
  teams: PropTypes.arrayOf(
    PropTypes.shape({
      slug: PropTypes.string,
      long_name: PropTypes.string,
    }),
  ).isRequired,
};

export default GoalKingWrapper;
