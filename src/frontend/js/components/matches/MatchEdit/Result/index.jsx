import { connect } from 'react-redux';
import { setMatchResult } from 'redux/actions/matchEditActions';
import Result from './Result';

const mapStateToProps = state => ({
  result: state.matchState.result,
});

const mapDispatchToProps = dispatch => ({
  onUpdateResult: (result) => {
    dispatch(setMatchResult(result));
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(Result);
