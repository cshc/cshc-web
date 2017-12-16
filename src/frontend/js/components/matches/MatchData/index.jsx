import { SwitchableView } from 'util/constants';
import switchable from 'components/common/ViewSwitcher/switchableView';
import MatchData from './MatchData';

export default switchable(SwitchableView.MatchList)(MatchData);
