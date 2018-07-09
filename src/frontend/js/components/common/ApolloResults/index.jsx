import React from 'react';
import PropTypes from 'prop-types';
import { NetworkStatus as NS } from 'apollo-client';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';

/**
 * A React Container that handles the networkStatus and error props provided
 * by an Apollo 'graphql' query container.
 * 
 * The container expects the query result to be passed to it as the 'data' prop.
 */
/* eslint-disable react/prefer-stateless-function */
const withApolloResults = (WrappedComponent) => {
  const ApolloResults = ({ networkStatus, error, data, loadingMessage, ...props }) => {
    if (error) return <ErrorDisplay errorMessage="Failed to load data" />;
    if (!data && networkStatus === NS.loading) {
      return <Loading message={loadingMessage} />;
    }
    return <WrappedComponent {...props} data={data} />;
  };

  ApolloResults.propTypes = {
    loadingMessage: PropTypes.string,
    networkStatus: PropTypes.number.isRequired,
    error: PropTypes.instanceOf(Error),
    data: PropTypes.oneOfType([PropTypes.shape(), PropTypes.arrayOf(PropTypes.shape())]),
  };

  ApolloResults.defaultProps = {
    loadingMessage: 'Fetching data...',
    error: undefined,
    data: undefined,
  };

  return ApolloResults;
};

export default withApolloResults;
