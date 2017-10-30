import { connect } from 'react-redux';

const mapStateToProps = state => ({
  activeFilters: state.ui.activeFilters,
});

export default connect(mapStateToProps);
