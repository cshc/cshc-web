import { connect } from 'react-redux';
import { updateAppearance, removeAppearance } from 'redux/actions/matchEditActions';
import Appearance from './Appearance';

const mapDispatchToProps = dispatch => ({
  onUpdateAppearance: (index, appearance) => {
    dispatch(updateAppearance(index, appearance));
  },
  onRemoveAppearance: (index) => {
    dispatch(removeAppearance(index));
  },
});

export default connect(null, mapDispatchToProps)(Appearance);
