import React from 'react';
import PropTypes from 'prop-types';
import MatchTimelineCard from './MatchTimelineCard';

/**
 * Representation of a list of matches as a timeline.
 * 
 * Ref: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/shortcode-blocks-timelines.html#shortcode2
 */
const MatchTimeline = ({ matches, exclude, dateFormat }) => (
  <ul className="row u-timeline-v2-wrap list-unstyled">
    {matches.map(match => (
      <MatchTimelineCard key={match.id} match={match} exclude={exclude} dateFormat={dateFormat} />
    ))}
  </ul>
);

MatchTimeline.propTypes = {
  matches: PropTypes.arrayOf(PropTypes.shape()).isRequired,
  exclude: PropTypes.arrayOf(PropTypes.string),
  dateFormat: PropTypes.string,
};

MatchTimeline.defaultProps = {
  exclude: [],
  dateFormat: 'Do MMM',
};

export default MatchTimeline;
