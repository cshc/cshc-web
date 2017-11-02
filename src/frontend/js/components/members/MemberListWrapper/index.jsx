import { compose } from 'react-apollo';
import switchable from 'components/common/ViewSwitcher/switchableView';
import filterable from 'components/filters/filterableContainer';
import { SwitchableView } from 'util/constants';
import MemberListQuery from './memberListQuery';
import MemberListWrapper from './MemberListWrapper';

const SwitchableVenueListView = switchable(SwitchableView.MemberList);

export default compose(filterable, MemberListQuery, SwitchableVenueListView)(MemberListWrapper);
