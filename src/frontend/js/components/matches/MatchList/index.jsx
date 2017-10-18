import { connect } from 'react-redux';
import { setViewType } from 'redux/actions/uiActions';
import { SwitchableView } from 'util/constants';
import MatchList from './MatchList';

const mapStateToProps = state => ({
  viewType: state.ui.viewTypes[SwitchableView.MatchList],
});

const mapDispatchToProps = dispatch => ({
  onSelectViewType: (viewType) => {
    dispatch(setViewType(SwitchableView.MatchList, viewType));
  },
});

export default connect(mapStateToProps, mapDispatchToProps)(MatchList);
