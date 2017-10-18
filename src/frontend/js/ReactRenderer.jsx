import React from 'react';
import ReactDOM from 'react-dom';
import { ApolloProvider } from 'react-apollo';
import { AppContainer } from 'react-hot-loader';
import { persistStore } from 'redux-persist';
import client from './network/client';
import buildStore from './redux/store';

export default (Component, reducers = {}, initialState, props = window.props) => {
  const store = buildStore(reducers, initialState, client);
  persistStore(store);
  ReactDOM.render(
    <AppContainer>
      <ApolloProvider store={store} client={client}>
        <Component {...props} />
      </ApolloProvider>
    </AppContainer>,
    window.react_mount,
  );
};
