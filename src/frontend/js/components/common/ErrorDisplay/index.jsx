import React from 'react';
import PropTypes from 'prop-types';

/**
 * Standard error display - primarily used when something goes wrong fetching GraphQL 
 * data through Apollo.
 * 
 * Note: Error messages should be user-friendly!
 */
const ErrorDisplay = ({ errorMessage }) => (
  <div className="g-mb-20 g-mt-20 g-flex-centered">
    <div className="g-flex-centered-item g-text-center">
      <i className="fas fa-exclamation-circle g-mr-5" />
      {errorMessage}
    </div>
  </div>
);

ErrorDisplay.propTypes = {
  errorMessage: PropTypes.string.isRequired,
};

module.exports = ErrorDisplay;
