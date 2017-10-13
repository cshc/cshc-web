import { connect } from 'react-redux';
import { setMatchViewType } from 'redux/actions/matchActions';
import MatchList from './MatchList';

const mapStateToProps = state => ({
  viewType: state.matches.viewType,
});

const mapDispatchToProps = dispatch => ({
  onSelectViewType: (viewType) => {
    dispatch(setMatchViewType(viewType));
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(MatchList);
