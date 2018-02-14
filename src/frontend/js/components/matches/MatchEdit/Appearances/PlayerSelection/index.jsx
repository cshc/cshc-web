import { connect } from 'react-redux';
import { addAppearance } from 'redux/actions/matchEditActions';
import PlayerSelection from './PlayerSelection';

const mapDispatchToProps = dispatch => ({
  onAddAppearance: (memberId, memberName) => {
    dispatch(addAppearance(memberId, memberName));
  },
});

export default connect(undefined, mapDispatchToProps)(PlayerSelection);
