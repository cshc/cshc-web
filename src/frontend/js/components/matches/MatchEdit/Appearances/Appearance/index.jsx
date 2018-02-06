import { connect } from 'react-redux';
import Appearance from './Appearance';
import { updateAppearance, removeAppearance } from 'redux/actions/matchEditActions';

const mapDispatchToProps = dispatch => ({
  onUpdateAppearance: (index, appearance) => {
    dispatch(updateAppearance(index, appearance));
  },
  onRemoveAppearance: (index) => {
    dispatch(removeAppearance(index));
  },
});

export default connect(null, mapDispatchToProps)(Appearance);
