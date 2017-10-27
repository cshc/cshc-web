import { compose } from 'react-apollo';

import MatchListWithData from 'components/matches/MatchList/matchListQuery';
import OppositionClubDetail from './OppositionClubDetail';

export default compose(MatchListWithData)(OppositionClubDetail);
