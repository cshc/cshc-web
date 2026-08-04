import React from 'react';
import PropTypes from 'prop-types';

/**
 * Loading/spinner component - typically displayed while fetching GraphQL data using Apollo.
 */
const Loading = ({ message }) => (
  <div className="text-center g-py-50">
    <i className="fas fa-spinner fa-spin fa-3x g-color-primary"></i>
    {message && <p className="g-mt-20">{message}</p>}
  </div>
);

Loading.propTypes = {
  message: PropTypes.string,
};

Loading.defaultProps = {
  message: undefined,
};

module.exports = Loading;
