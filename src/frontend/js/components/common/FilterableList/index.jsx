import React from 'react';
import PropTypes from 'prop-types';

const FilterableList = ({ filterSet, listWrapper }) => (
  <div className="row">
    <div className="col-12 col-lg-4">{filterSet}</div>
    <div className="col-12 col-lg-8">{listWrapper}</div>
  </div>
);

FilterableList.propTypes = {
  filterSet: PropTypes.node.isRequired,
  listWrapper: PropTypes.node.isRequired,
};

export default FilterableList;
