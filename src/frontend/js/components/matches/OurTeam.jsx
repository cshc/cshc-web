import React from 'react';
import PropTypes from 'prop-types';
import Urls from 'util/urls';

/**
 * Representation of a particular CSHC team and a link to the team details page.
 */
const OurTeam = ({ team }) => (
  <a title="View team details" href={Urls.clubteam_detail(team.slug)}>
    {team.shortName}
  </a>
);

OurTeam.propTypes = {
  team: PropTypes.shape({
    slug: PropTypes.string,
    shortName: PropTypes.string,
  }).isRequired,
};

export default OurTeam;
