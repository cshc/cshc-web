import React from 'react';
import ReactDOM from 'react-dom';
import { AppContainer } from 'react-hot-loader';
import Temp from './Temp';

ReactDOM.render(
  <AppContainer>
    <Temp text="Venue Details" />
  </AppContainer>,
  document.getElementById('react-app'),
);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('./Temp', () => {
    const NextApp = require('./Temp').default;
    ReactDOM.render(
      <AppContainer>
        <NextApp text="Venue Details" />
      </AppContainer>,
      document.getElementById('root'),
    );
  });
}
/* eslint-enable global-require */
