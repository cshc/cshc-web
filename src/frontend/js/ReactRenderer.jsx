import React from 'react';
import ReactDOM from 'react-dom';
import { ApolloProvider } from 'react-apollo';
import { AppContainer } from 'react-hot-loader';
import client from './network/client';
import buildStore from './redux/store';

export default (Component, reducers = {}, initialState, props = window.props) => {
  ReactDOM.render(
    <AppContainer>
      <ApolloProvider store={buildStore(reducers, initialState, client)} client={client}>
        <Component {...props} />
      </ApolloProvider>
    </AppContainer>,
    window.react_mount,
  );
};
