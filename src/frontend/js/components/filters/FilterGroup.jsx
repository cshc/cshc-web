import React from 'react';
import PropTypes from 'prop-types';
import Subheading from 'components/common/Subheading';

/**
 * A group of filters, with a title
 */
const FilterGroup = ({ title, description, children }) => (
  <div>
    <Subheading>{title}</Subheading>
    {description ? <p>{description}</p> : null}
    {children}
  </div>
);

FilterGroup.propTypes = {
  title: PropTypes.string.isRequired,
  description: PropTypes.string,
  children: PropTypes.node.isRequired,
};

FilterGroup.defaultProps = {
  description: undefined,
};

export default FilterGroup;
