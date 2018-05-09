import React from 'react';
import PropTypes from 'prop-types';
import Team from 'models/team';
import Urls from 'util/urls';

/**
 * Representation of a particular opposition club team and a link to the club details page.
 */
const OppositionTeam = ({ team }) => (
  <a title="View club details" href={Urls.opposition_club_detail(team.club.slug)}>
    {Team.genderlessName(team)}
  </a>
);

OppositionTeam.propTypes = {
  team: PropTypes.shape({
    name: PropTypes.string.isRequired,
    club: PropTypes.shape({
      slug: PropTypes.string.isRequired,
    }),
  }).isRequired,
};

export default OppositionTeam;
