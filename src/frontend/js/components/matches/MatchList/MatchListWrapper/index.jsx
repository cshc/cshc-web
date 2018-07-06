import { addUrlProps } from 'react-url-query';
import Paged from 'components/common/Paged';
import Orderable from 'components/common/Orderable';
import { urlPropsQueryConfig } from 'components/matches/MatchList/MatchFilterSet';
import MatchListWrapper from './MatchListWrapper';

const Filterable = addUrlProps({
  urlPropsQueryConfig: {
    ...urlPropsQueryConfig,
    ...Paged,
    ...Orderable,
  },
});

export default Filterable(MatchListWrapper);
