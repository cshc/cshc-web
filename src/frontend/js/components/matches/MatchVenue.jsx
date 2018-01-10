import React from 'react';
import PropTypes from 'prop-types';
import Match from 'models/match';
import Urls from 'util/urls';

/**
 * Representation and link to a particular venue.
 */
const MatchVenue = ({ match, simple }) => {
  if (!match.venue) {
    return Match.isPast(match) ? '???' : <abbr title="Venue not known">TBD</abbr>;
  }
  return (
    <a href={Urls.venue_detail(match.venue.slug)} title={match.venue.name}>
      {simple ? Match.simpleVenueName(match) : match.venue.shortName}
    </a>
  );
};

MatchVenue.propTypes = {
  match: PropTypes.shape({
    homeAway: PropTypes.string,
    venue: PropTypes.shape({
      shortName: PropTypes.string,
      name: PropTypes.string,
    }),
    date: PropTypes.string,
    time: PropTypes.string,
  }).isRequired,
  simple: PropTypes.bool,
};

MatchVenue.defaultProps = {
  simple: true,
};

export default MatchVenue;
