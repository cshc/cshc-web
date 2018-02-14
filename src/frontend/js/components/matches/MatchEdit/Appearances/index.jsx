import { connect } from 'react-redux';
import Appearances from './Appearances';

const mapStateToProps = state => ({
  playerOptions: state.matchState.playerOptions,
  result: state.matchState.result,
  appearances: state.matchState.appearances,
  teamGoals: state.matchState.result.ourScore,
});

export default connect(mapStateToProps)(Appearances);
