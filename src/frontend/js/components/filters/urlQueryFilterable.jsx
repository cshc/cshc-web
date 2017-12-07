import React from 'react';
import PropTypes from 'prop-types';
import { toTitleCase } from 'util/cshc';

const UrlQueryFilter = ({ Filter, ...props }) => {
  const onSetFilter = (filterName, filterValue) =>
    props[`onChange{${toTitleCase(filterName)}`](filterValue);
  return (
    <Filter
      {...props}
      filterValue={props[toTitleCase(props.filterName)]}
      onSetFilter={onSetFilter}
    />
  );
};

UrlQueryFilter.propTypes = {
  Filter: PropTypes.node.isRequired,
  filterName: PropTypes.string.isRequired,
};

export default UrlQueryFilter;
