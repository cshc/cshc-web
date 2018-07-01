import React from 'react';
import ReactDOM from 'react-dom';
import { ApolloProvider } from 'react-apollo';
import { Provider } from 'react-redux';
import { AppContainer } from 'react-hot-loader';
import { BrowserRouter as Router } from 'react-router-dom';
import { RouterToUrlQuery } from 'react-url-query';
import { persistStore } from 'redux-persist';
import { PersistGate } from 'redux-persist/es/integration/react';
import PersistLoading from 'components/common/PersistLoading';
import getClient from './network/client';
import buildStore from './redux/store';

/**
 * Reusable method to render the root component structure for a React App.
 * 
 * Note: if props are not explicitly supplied, it is assumed they are 
 * located in a 'window.props' object.
 */
export default (Component, reducers = {}, initialState, baseUrl = '/', props = window.props) => {
  const store = buildStore(Component.name, reducers, initialState);

  ReactDOM.render(
    <AppContainer>
      <ApolloProvider client={getClient(store)}>
        <Provider store={store}>
          <PersistGate loading={<PersistLoading />} persistor={persistStore(store)}>
            <Router basename={baseUrl}>
              <RouterToUrlQuery>
                <Component {...props} />
              </RouterToUrlQuery>
            </Router>
          </PersistGate>
        </Provider>
      </ApolloProvider>
    </AppContainer>,
    window.react_mount,
  );
};
