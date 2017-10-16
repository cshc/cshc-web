import React from 'react';
import PropTypes from 'prop-types';

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
