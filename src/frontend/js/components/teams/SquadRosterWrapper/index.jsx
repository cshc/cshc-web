import { compose } from 'react-apollo';
import switchable from 'components/common/ViewSwitcher/switchableView';
import filterable from 'components/filters/filterableContainer';
import { SwitchableView } from 'util/constants';
import SquadRosterWrapper from './SquadRosterWrapper';

const SwitchableSquadRoster = switchable(SwitchableView.SquadRoster);

export default compose(filterable, SwitchableSquadRoster)(SquadRosterWrapper);
