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
  let iconClassName = `${className} fa `;
  if (match.hasReport) iconClassName += 'fa-file-text';
  else if (Match.finalScoresProvided(match)) iconClassName += 'fa-file';
  else iconClassName += 'fa-file-o';
  return (
    <a href={Urls.match_detail(match.modelId)} title="Match details">
      <span className="u-icon-v1 u-icon-effect-v1-2--hover g-rounded-3">
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
