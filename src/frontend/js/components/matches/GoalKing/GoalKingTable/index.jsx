import { compose } from 'react-apollo';
import { addUrlProps } from 'react-url-query';
import GoalKingQuery from './goalKingQuery';
import GoalKingTable from './GoalKingTable';
import { urlPropsQueryConfig } from '../GoalKingFilterSet';

export default compose(addUrlProps({ urlPropsQueryConfig }), GoalKingQuery)(GoalKingTable);
