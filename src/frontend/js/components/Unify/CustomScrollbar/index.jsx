import React from 'react';
import PropTypes from 'prop-types';
import classnames from 'classnames';

/**
 * Represents a custom scrollbar.
 * 
 * Notes: 
 *  - jquery.mCustomScrollbar.min.css must be included in the page head
 *  - jquery.min.js and jquery.mCustomScrollbar.concat.min.js must be included in the body
 *  - Assumes window.jQuery is accessible
 * 
 * Ref: http://manos.malihu.gr/jquery-custom-content-scroller/
 */
class CustomScrollbar extends React.Component {
  componentDidMount() {
    window.jQuery('.mCustomScrollbar').mCustomScrollbar();
  }

  render() {
    const { maxHeight, className, children } = this.props;
    const divClass = classnames(
      'js-scrollbar u-info-v1-1 g-bg-white-gradient-v1--after mCustomScrollbar',
      className,
    );
    return (
      <div
        ref={(scrollbar) => {
          this.scrollbar = scrollbar;
        }}
        className={divClass}
        style={maxHeight ? { maxHeight } : {}}
        data-mcs-theme="minimal-dark"
      >
        {children}
      </div>
    );
  }
}

CustomScrollbar.propTypes = {
  className: PropTypes.string,
  maxHeight: PropTypes.string,
  children: PropTypes.node.isRequired,
};

CustomScrollbar.defaultProps = {
  className: undefined,
  maxHeight: '200px',
};

export default CustomScrollbar;
