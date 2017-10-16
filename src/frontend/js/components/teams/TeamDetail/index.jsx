import { compose } from 'react-apollo';

import MatchListWithData from 'components/matches/MatchList/matchListQuery';
import TeamDetail from './TeamDetail';

export default compose(MatchListWithData)(TeamDetail);
