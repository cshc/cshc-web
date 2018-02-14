import { connect } from 'react-redux';
import { updateAwardWinner, removeAwardWinner } from 'redux/actions/matchEditActions';
import AwardWinner from './AwardWinner';

const mapDispatchToProps = dispatch => ({
  onUpdateAwardWinner: (awardWinner, index) => {
    dispatch(updateAwardWinner(awardWinner, index));
  },
  onRemoveAwardWinner: (index) => {
    dispatch(removeAwardWinner(index));
  },
});

export default connect(null, mapDispatchToProps)(AwardWinner);
