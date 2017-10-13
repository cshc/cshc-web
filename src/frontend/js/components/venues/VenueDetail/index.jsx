import { compose } from 'react-apollo';

import MatchListWithData from 'components/matches/MatchList/matchListQuery';
import VenueDetail from './VenueDetail';

export default compose(MatchListWithData)(VenueDetail);
