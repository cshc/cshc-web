import { connect } from 'react-redux';
import { setDataFilter } from 'redux/actions/uiActions';

const mapStateToProps = (state, ownProps) => ({
  filterValue: state.ui.activeFilters[ownProps.filterName],
  ...ownProps,
});

const mapDispatchToProps = dispatch => ({
  onSetFilter: (filterName, filterValue) => {
    dispatch(setDataFilter(filterName, filterValue));
  },
});

export default connect(mapStateToProps, mapDispatchToProps);
