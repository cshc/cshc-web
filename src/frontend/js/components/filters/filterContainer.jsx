import { connect } from 'react-redux';
import { setDataFilter } from 'redux/actions/uiActions';

const mapStateToProps = filterName => state => ({
  filterValue: state.ui.activeFilters[filterName],
  filterName,
});

const mapDispatchToProps = dispatch => ({
  onSetFilter: (filterName, filterValue) => {
    dispatch(setDataFilter(filterName, filterValue));
  },
});

export default filterName => connect(mapStateToProps(filterName), mapDispatchToProps);
