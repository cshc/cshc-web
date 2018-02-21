import React from 'react';
import PropTypes from 'prop-types';
import Match from 'models/match';
import Urls from 'util/urls';

/**
 * Link to a particular match. 
 * 
 * The icon reflects the status of the details known about the match.
 */
const MatchLink = ({ match, className }) => {
  let iconClassName = `${className} `;
  if (match.hasReport) iconClassName += 'fas fa-file-alt';
  else if (Match.finalScoresProvided(match)) iconClassName += 'far fa-file';
  else iconClassName += 'fas fa-file';
  return (
    <a href={Urls.match_detail(match.id)} title="Match details">
      <span className="u-icon-v1 g-bg-primary--hover g-color-white--hover">
        <i className={iconClassName} />
      </span>
    </a>
  );
};

MatchLink.propTypes = {
  match: PropTypes.shape({
    hasReport: PropTypes.bool,
    ourScore: PropTypes.number,
    oppScore: PropTypes.number,
  }).isRequired,
  className: PropTypes.string,
};

MatchLink.defaultProps = {
  className: '',
};

export default MatchLink;
