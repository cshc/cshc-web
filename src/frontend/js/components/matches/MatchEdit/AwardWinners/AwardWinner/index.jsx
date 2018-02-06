import { connect } from 'react-redux';
import AwardWinner from './AwardWinner';
import { updateAwardWinner, removeAwardWinner } from 'redux/actions/matchEditActions';

const mapDispatchToProps = dispatch => ({
  onUpdateAwardWinner: (awardWinner, index) => {
    dispatch(updateAwardWinner(awardWinner, index));
  },
  onRemoveAwardWinner: (index) => {
    dispatch(removeAwardWinner(index));
  },
});

export default connect(null, mapDispatchToProps)(AwardWinner);
