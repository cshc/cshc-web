import React from 'react';
import PropTypes from 'prop-types';

const ErrorDisplay = ({ errorMessage }) => (
  <div className="g-mb-20 g-mt-20 g-flex-centered">
    <div className="g-flex-centered-item g-text-center">
      <i className="fa fa-exclamation-circle g-mr-5" />
      {errorMessage}
    </div>
  </div>
);

ErrorDisplay.propTypes = {
  errorMessage: PropTypes.string.isRequired,
};

module.exports = ErrorDisplay;
