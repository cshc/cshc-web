import React from 'react';
import render from '../ReactRenderer';
import style from './VenueDetails.scss';

const VenueDetails = () => <h1 className={style.details}>Venue Details</h1>;

render(VenueDetails);

/* eslint-disable global-require */
// Hot Module Replacement API
// if (module.hot) {
//   module.hot.accept('./Temp', () => {
//     const NextApp = require('./Temp').default;
//     render(NextApp);
//   });
// }
/* eslint-enable global-require */
