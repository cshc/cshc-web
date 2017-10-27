import React from 'react';
import PropTypes from 'prop-types';

/**
 * Very simple component to represent thw indicator that away kit should be worn
 * 
 * (e.g. when the opposing team's kit clashes with ours and we're playing away)
 * 
 * Note: The logic to determine whether away kit should be worn as a result of a 
 * kit clash for a particular match is encapsulated in the Match Django model itself.
 */
const KitClashIcon = ({ match }) => {
  if (!match.kitClash) return null;
  return <i className="fa fa-user g-ml-5" title="Away kit" />;
};

KitClashIcon.propTypes = {
  match: PropTypes.shape({
    kitClash: PropTypes.bool,
  }).isRequired,
};

export default KitClashIcon;
