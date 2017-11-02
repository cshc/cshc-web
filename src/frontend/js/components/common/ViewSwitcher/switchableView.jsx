import { connect } from 'react-redux';
import { setViewType } from 'redux/actions/uiActions';

const mapStateToProps = viewName => state => ({
  viewType: state.ui.viewTypes[viewName],
});

const mapDispatchToProps = viewName => dispatch => ({
  onSelectViewType: (viewType) => {
    dispatch(setViewType(viewName, viewType));
  },
});

export default viewName => connect(mapStateToProps(viewName), mapDispatchToProps(viewName));
