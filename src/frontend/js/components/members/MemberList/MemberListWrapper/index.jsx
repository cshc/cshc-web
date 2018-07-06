import { compose } from 'react-apollo';
import switchable from 'components/common/ViewSwitcher/switchableView';
import { addUrlProps } from 'react-url-query';
import Paged from 'components/common/Paged';
import { SwitchableView } from 'util/constants';
import MemberListQuery from './memberListQuery';
import MemberListWrapper from './MemberListWrapper';
import { urlPropsQueryConfig } from '../MemberFilterSet';

const SwitchableVenueListView = switchable(SwitchableView.MemberList);

const withUrlProps = addUrlProps({
  urlPropsQueryConfig: {
    ...urlPropsQueryConfig,
    ...Paged,
  },
});

export default compose(withUrlProps, MemberListQuery, SwitchableVenueListView)(MemberListWrapper);
