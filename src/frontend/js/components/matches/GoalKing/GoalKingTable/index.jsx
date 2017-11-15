import { compose } from 'react-apollo';
import filterable from 'components/filters/filterableContainer';
import GoalKingQuery from './goalKingQuery';
import GoalKingTable from './GoalKingTable';

export default compose(filterable, GoalKingQuery)(GoalKingTable);
