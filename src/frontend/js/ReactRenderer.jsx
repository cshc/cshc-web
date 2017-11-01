import React from 'react';
import ReactDOM from 'react-dom';
import { ApolloProvider } from 'react-apollo';
import { AppContainer } from 'react-hot-loader';
import { persistStore } from 'redux-persist';
import { PersistGate } from 'redux-persist/es/integration/react';
import Loading from 'components/common/Loading';
import client from './network/client';
import buildStore from './redux/store';

/**
 * Reusable method to render the root component structure for a React App.
 * 
 * Note: if props are not explicitly supplied, it is assumed they are 
 * located in a 'window.props' object.
 */
export default (Component, reducers = {}, initialState, props = window.props) => {
  const store = buildStore(Component.name, reducers, initialState, client);

  ReactDOM.render(
    <AppContainer>
      <ApolloProvider store={store} client={client}>
        <PersistGate loading={<Loading />} persistor={persistStore(store)}>
          <Component {...props} />
        </PersistGate>
      </ApolloProvider>
    </AppContainer>,
    window.react_mount,
  );
};
