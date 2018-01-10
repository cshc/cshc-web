import { compose } from 'react-apollo';
import { addUrlProps } from 'react-url-query';
import Paged from 'components/common/Paged';
import Orderable from 'components/common/Orderable';
import { urlPropsQueryConfig } from 'components/matches/MatchList/MatchFilterSet';
import MatchListWrapper from './MatchListWrapper';

const Filterable = addUrlProps({ urlPropsQueryConfig });

export default compose(Paged, Orderable, Filterable)(MatchListWrapper);
