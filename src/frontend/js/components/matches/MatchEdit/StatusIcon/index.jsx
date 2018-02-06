import React from 'react';
import PropTypes from 'prop-types';

const StatusIcon = ({ error }) => (error ? (
  <i className="fa fa-exclamation-circle g-color-yellow" />
) : (
  <i className="fa fa-check-square g-color-green" />
));

StatusIcon.propTypes = {
  error: PropTypes.bool.isRequired,
};

export default StatusIcon;
