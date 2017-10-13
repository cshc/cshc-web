import React from 'react';
import PropTypes from 'prop-types';
import Team from 'models/team';

const OppositionTeam = ({ team }) => (
  <a title="View club details" href="#">
    {Team.genderlessName(team)}
  </a>
);

OppositionTeam.propTypes = {
  team: PropTypes.shape({
    name: PropTypes.string,
  }).isRequired,
};

export default OppositionTeam;
