import { compose } from 'react-apollo';
import { addUrlProps } from 'react-url-query';
import Paged from 'components/common/Paged';
import Orderable from 'components/common/Orderable';
import { urlPropsQueryConfig } from 'components/awards/EndOfSeasonAwardWinnerList/EosFilterSet';
import EosListWithData from './eosQuery';
import EosListDisplay from './EosListDisplay';

const Filterable = addUrlProps({ urlPropsQueryConfig });

export default compose(Paged, Orderable, Filterable, EosListWithData)(EosListDisplay);
