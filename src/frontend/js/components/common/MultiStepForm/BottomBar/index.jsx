import React from 'react';
import PropTypes from 'prop-types';
import StickyBar from 'components/common/StickyBar';
import { SlideListPropType } from '../PropTypes';

/**
 *  The sticky bar at the bottom of a multi-step form that contains the 
 *  prev/next navigation and child content in the middle of the bar.
 * 
 */
class MultiStepFormBottomBar extends React.PureComponent {
  constructor(props) {
    super(props);
    this.state = {
      currentSlideIndex: 0,
    };
  }

  onSlideChange(oldIndex, newIndex) {
    this.setState({ currentSlideIndex: newIndex });
  }

  render() {
    const { slides, onClickPrevious, onClickNext, children } = this.props;
    const { currentSlideIndex } = this.state;
    return (
      <StickyBar
        style={{ bottom: 0 }}
        className="container g-z-index-99 d-flex g-bg-gray-light-v4 justify-content-between g-py-10"
      >
        <div className="flex-1">
          {currentSlideIndex > 0 ? (
            <button onClick={onClickPrevious} className="btn btn-link">
              <i className="fas fa-chevron-left g-mr-5" />
              {slides[currentSlideIndex - 1].label}
            </button>
          ) : null}
        </div>
        <div className="flex-0-auto">{children}</div>
        <div className="flex-1 text-right">
          {currentSlideIndex < slides.length - 1 ? (
            <button onClick={onClickNext} className="btn btn-link">
              {slides[currentSlideIndex + 1].label}
              <i className="fas fa-chevron-right g-ml-5" />
            </button>
          ) : null}
        </div>
      </StickyBar>
    );
  }
}

MultiStepFormBottomBar.propTypes = {
  slides: SlideListPropType.isRequired,
  onClickPrevious: PropTypes.func.isRequired,
  onClickNext: PropTypes.func.isRequired,
  children: PropTypes.node,
};

MultiStepFormBottomBar.defaultProps = {
  children: undefined,
};

export default MultiStepFormBottomBar;
