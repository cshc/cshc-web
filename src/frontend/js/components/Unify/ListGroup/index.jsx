import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';
import ListGroupItem from './ListGroupItem';

/**
 * Represents a List Group
 * 
 * Ref: https://htmlstream.com/preview/unify-v2.2/unify-main/shortcodes/shortcode-base-lists-group.html
 */
const ListGroup = ({ className, children }) => {
  if (!children) return null;
  return (
    <div className={classnames('list-group list-group-border-0 g-mb-40', className)}>
      {children}
    </div>
  );
};

ListGroup.propTypes = {
  className: PropTypes.string,
  children: PropTypes.arrayOf(ListGroupItem),
};

ListGroup.defaultProps = {
  className: undefined,
  children: undefined,
};

export default ListGroup;
