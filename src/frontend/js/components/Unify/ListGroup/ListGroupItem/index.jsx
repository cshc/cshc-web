import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';

/**
 * Represents a List Group Item within a List Group
 */
const ListGroupItem = ({ isActive, children }) => {
  const listItemClass = classnames('list-group-item', {
    active: isActive,
  });
  return <div className={listItemClass}>{children}</div>;
};

ListGroupItem.propTypes = {
  isActive: PropTypes.bool.isRequired,
  children: PropTypes.node,
};

ListGroupItem.defaultProps = {
  children: undefined,
};

export default ListGroupItem;
