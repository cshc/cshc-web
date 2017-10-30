import { connect } from 'react-redux';
import { setViewType } from 'redux/actions/uiActions';

const mapStateToProps = viewName => state => ({
  viewType: state.ui.viewTypes[viewName],
});

const mapDispatchToProps = dispatch => ({
  onSelectViewType: (viewName, viewType) => {
    dispatch(setViewType(viewName, viewType));
  },
});

export default viewName => connect(mapStateToProps(viewName), mapDispatchToProps);
