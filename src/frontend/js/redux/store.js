import { createStore, applyMiddleware, compose } from 'redux';
import { persistCombineReducers, purgeStoredState } from 'redux-persist';
import storage from 'redux-persist/es/storage'; // default: localStorage if web, AsyncStorage if react-native
import Urls from 'util/urls';

/* eslint-disable no-underscore-dangle */
const buildStore = (key, reducers, initialState, client) => {
  const persistConfig = {
    key,
    storage,
  };
  if (Urls.getParameterByName('purge')) {
    purgeStoredState(persistConfig);
  }
  const persistedReducers = persistCombineReducers(persistConfig, {
    ...reducers,
    apollo: client.reducer(),
  });
  return createStore(
    persistedReducers,
    initialState,
    compose(
      applyMiddleware(client.middleware()),
      typeof window.__REDUX_DEVTOOLS_EXTENSION__ !== 'undefined'
        ? window.__REDUX_DEVTOOLS_EXTENSION__()
        : f => f,
    ),
  );
};

/* eslint-enable no-underscore-dangle */
module.exports = buildStore;
