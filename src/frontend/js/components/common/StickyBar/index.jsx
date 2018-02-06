import React from 'react';
import PropTypes from 'prop-types';
import Stickyfill from 'stickyfilljs';
import classnames from 'classnames';
import './style.scss';

/**
 * A sticky container that sticks at the top (determined by the 'top' prop value) when 
 * the view is scrolled up.
 * 
 * Note: "position: sticky" only has limited browser support at the moment so we use this
 * polyfill as well: https://github.com/wilddeer/stickyfill 
 */
class StickyBar extends React.Component {
  componentDidMount() {
    const elements = document.querySelectorAll('.sticky');
    Stickyfill.add(elements);
  }

  render() {
    const cn = classnames('sticky', this.props.className);
    // const inlineStyle = { top: `${this.props.top}px` };
    return <div className={cn}>{this.props.children}</div>;
  }
}

StickyBar.propTypes = {
  children: PropTypes.node.isRequired,
  className: PropTypes.string,
  top: PropTypes.number,
};

StickyBar.defaultProps = {
  className: undefined,
  top: 0,
};

export default StickyBar;
