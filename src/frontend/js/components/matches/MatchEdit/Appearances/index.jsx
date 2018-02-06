import { connect } from 'react-redux';
import Appearances from './Appearances';

const mapStateToProps = state => ({
  playerOptions: state.matchState.playerOptions,
  appearances: state.matchState.appearances,
});

export default connect(mapStateToProps)(Appearances);
