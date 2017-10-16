import { compose } from 'react-apollo';

import LeagueTableWithData from './leagueTableQuery';
import LeagueTable from './LeagueTable';

export default compose(LeagueTableWithData)(LeagueTable);
