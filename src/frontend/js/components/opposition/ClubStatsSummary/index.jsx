import { compose } from 'react-apollo';

import ClubStatsSummaryWithData from './clubStatsSummaryQuery';
import ClubStatsSummary from './ClubStatsSummary';

export default compose(ClubStatsSummaryWithData)(ClubStatsSummary);
