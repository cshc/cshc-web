import { compose } from 'react-apollo';
import switchable from 'components/common/ViewSwitcher/switchableView';
import { addUrlProps, UrlQueryParamTypes } from 'react-url-query';
import Paged from 'components/common/Paged';
import { SwitchableView } from 'util/constants';
import MemberListQuery from './memberListQuery';
import MemberListWrapper from './MemberListWrapper';
import { urlPropsQueryConfig } from '../MemberFilterSet';

const SwitchableVenueListView = switchable(SwitchableView.MemberList);

// Custom URL param type for sorting
const SortUrlParam = {
  encode: (sorted) => {
    if (!sorted || sorted.length === 0) return undefined;
    const sort = sorted[0]; // Only support single column sort
    return sort.desc ? `-${sort.id}` : sort.id;
  },
  decode: (sortString) => {
    if (!sortString) return [];
    const desc = sortString.startsWith('-');
    const id = desc ? sortString.substring(1) : sortString;
    return [{ id, desc }];
  },
};

const withUrlProps = addUrlProps({
  urlPropsQueryConfig: {
    ...urlPropsQueryConfig,
    ...Paged,
    sorted: {
      type: SortUrlParam,
      queryParam: 'sort',
    },
  },
});

export default compose(withUrlProps, MemberListQuery, SwitchableVenueListView)(MemberListWrapper);
