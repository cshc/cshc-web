import render from 'ReactRenderer';
import MatchList from 'components/matches/MatchList';

render(MatchList);

/* eslint-disable global-require */
// Hot Module Replacement API
if (module.hot) {
  module.hot.accept('../components/matches/MatchList', () => {
    const NewMatchList = require('../components/matches/MatchList').default;
    render(NewMatchList);
  });
}
/* eslint-enable global-require */
