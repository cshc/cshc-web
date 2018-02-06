import { connect } from 'react-redux';
import { addAwardWinner } from 'redux/actions/matchEditActions';
import AwardWinners from './AwardWinners';

const mapStateToProps = state => ({
  memberOptions: state.matchState.playerOptions,
  awardWinners: state.matchState.awardWinners,
});

const mapDispatchToProps = dispatch => ({
  onAddAwardWinner: () => {
    dispatch(addAwardWinner());
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(AwardWinners);
