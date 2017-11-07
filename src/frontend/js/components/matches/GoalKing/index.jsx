import { compose } from 'react-apollo';
import filterable from 'components/filters/filterableContainer';
import GoalKingQuery from './goalKingQuery';
import GoalKingWrapper from './GoalKingWrapper';

export default compose(filterable, GoalKingQuery)(GoalKingWrapper);
