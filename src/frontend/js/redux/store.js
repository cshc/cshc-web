import { createStore, combineReducers, applyMiddleware, compose } from 'redux';

/* eslint-disable no-underscore-dangle */
const buildStore = (reducers, initialState, client) =>
  createStore(
    combineReducers({
      ...reducers,
      apollo: client.reducer(),
    }),
    initialState,
    compose(
      applyMiddleware(client.middleware()),
      // If you are using the devToolsExtension, you can add it here also
      typeof window.__REDUX_DEVTOOLS_EXTENSION__ !== 'undefined'
        ? window.__REDUX_DEVTOOLS_EXTENSION__()
        : f => f,
    ),
  );

/* eslint-enable no-underscore-dangle */
module.exports = buildStore;
