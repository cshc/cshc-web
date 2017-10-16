import { compose } from 'react-apollo';

import SquadRosterQuery from './squadRosterQuery';
import SquadRoster from './SquadRoster';

export default compose(SquadRosterQuery)(SquadRoster);
