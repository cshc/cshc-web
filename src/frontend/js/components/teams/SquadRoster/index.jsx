import { compose } from 'react-apollo';
import switchable from 'components/common/ViewSwitcher/switchableView';
import { SwitchableView } from 'util/constants';
import SquadRosterQuery from './squadRosterQuery';
import SquadRoster from './SquadRoster';

const SwitchableSquadRosterView = switchable(SwitchableView.SquadRoster);

export default compose(SquadRosterQuery, SwitchableSquadRosterView)(SquadRoster);
