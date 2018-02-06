import { connect } from 'react-redux';
import Result from './Result';
import { setMatchResult } from 'redux/actions/matchEditActions';

const mapStateToProps = state => ({
  result: state.matchState.result,
});

const mapDispatchToProps = dispatch => ({
  onUpdateResult: (result) => {
    dispatch(setMatchResult(result));
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(Result);
