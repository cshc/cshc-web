import { connect } from 'react-redux';
import { setMatchReport } from 'redux/actions/matchEditActions';
import Report from './Report';

const mapStateToProps = state => ({
  authorOptions: state.matchState.playerOptions,
  report: state.matchState.report,
});

const mapDispatchToProps = dispatch => ({
  onUpdateReport: (report) => {
    dispatch(setMatchReport(report));
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(Report);
