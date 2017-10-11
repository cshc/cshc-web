/* @flow */

import { compose } from 'react-apollo';

import MatchListWithData from './matchListQuery';
import MatchList from './MatchList';

export default compose(MatchListWithData)(MatchList);
