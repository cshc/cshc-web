import { connect } from 'react-redux';
import { compose } from 'react-apollo';
import UpdateMatchMutation from './updateMatchMutation';
import MatchEditTopBar from './MatchEditTopBar';

const mapStateToProps = state => ({
  matchState: state.matchState,
});

export default compose(connect(mapStateToProps), UpdateMatchMutation)(MatchEditTopBar);
