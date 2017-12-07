import React from 'react';
import PropTypes from 'prop-types';
import ListGroupItem from './ListGroupItem';

/**
 * Represents a List Group
 * 
 * Ref: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/shortcode-base-lists-group.html
 */
const ListGroup = ({ children }) => {
  if (!children) return null;
  return <div className="list-group list-group-border-0 g-mb-40">{children}</div>;
};

ListGroup.propTypes = {
  children: PropTypes.arrayOf(ListGroupItem),
};

ListGroup.defaultProps = {
  children: undefined,
};

export default ListGroup;
