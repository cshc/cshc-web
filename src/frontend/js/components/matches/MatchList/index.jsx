import { SwitchableView } from 'util/constants';
import switchable from 'components/common/ViewSwitcher/switchableView';
import MatchList from './MatchList';

export default switchable(SwitchableView.MatchList)(MatchList);
