import { connect } from 'react-redux';
import PlayerSelection from './PlayerSelection';
import { addAppearance } from 'redux/actions/matchEditActions';

const mapDispatchToProps = dispatch => ({
  onAddAppearance: (memberId, memberName) => {
    dispatch(addAppearance(memberId, memberName));
  },
});

export default connect(undefined, mapDispatchToProps)(PlayerSelection);
