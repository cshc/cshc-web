import { compose } from 'react-apollo';
import { connect } from 'react-redux';
import { setViewType } from 'redux/actions/uiActions';
import { SwitchableView } from 'util/constants';
import SquadRosterQuery from './squadRosterQuery';
import SquadRoster from './SquadRoster';

const mapStateToProps = state => ({
  viewType: state.ui.viewTypes[SwitchableView.SquadRoster],
});

const mapDispatchToProps = dispatch => ({
  onSelectViewType: (viewType) => {
    dispatch(setViewType(SwitchableView.SquadRoster, viewType));
  },
});

const SwitchableSquadRosterView = connect(mapStateToProps, mapDispatchToProps);

export default compose(SquadRosterQuery, SwitchableSquadRosterView)(SquadRoster);
