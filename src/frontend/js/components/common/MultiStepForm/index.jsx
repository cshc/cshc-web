import React from 'react';
import PropTypes from 'prop-types';
import reduce from 'lodash/reduce';
import Slider from 'react-slick';
import { Panel } from 'components/Unify';
import { SlideListPropType } from './PropTypes';
import MultiStepFormBottomBar from './BottomBar';
import MultiStepFormNavigation from './Navigation';

const panelProps = {
  outlineColor: 'primary',
  headerColor: 'primary',
};

/**
 * Generic multi-step form.
 * 
 * The form consists of the following:
 * 1. a row of Navigation Nodes
 * 2. A Slider where each 'slider child' is wrapped in a Panel
 * 3. A bottom navigation bar with optional action buttons.
 */
class MultiStepForm extends React.PureComponent {
  constructor(props) {
    super(props);
    this.updateIndex = this.updateIndex.bind(this);
  }

  updateIndex(oldIndex, newIndex) {
    this.nav.onSlideChange(oldIndex, newIndex);
    this.bottomBar.onSlideChange(oldIndex, newIndex);
  }

  goToSlide(slideIndex) {
    this.slider.slickGoTo(slideIndex);
  }

  render() {
    const { slides, children, bottomBarActions, panelClass } = this.props;

    const sliderChildren = reduce(
      slides,
      (acc, slide, index) => {
        acc.push(
          <div key={slide.label}>
            <Panel
              {...panelProps}
              className={panelClass}
              title={slide.title || slide.label}
              icon={slide.icon}
            >
              {children[index]}
            </Panel>
          </div>,
        );
        return acc;
      },
      [],
    );

    return (
      <div>
        <MultiStepFormNavigation
          ref={(c) => {
            this.nav = c;
          }}
          slides={slides}
          onSelectSlide={(index) => {
            this.slider.slickGoTo(index);
          }}
        />
        <Slider
          ref={(c) => {
            this.slider = c;
          }}
          dots={false}
          arrows={false}
          infinite={false}
          draggable={false}
          adaptiveHeight
          beforeChange={this.updateIndex}
        >
          {sliderChildren}
        </Slider>
        <MultiStepFormBottomBar
          ref={(c) => {
            this.bottomBar = c;
          }}
          slides={slides}
          onClickPrevious={() => {
            this.slider.slickPrev();
          }}
          onClickNext={() => {
            this.slider.slickNext();
          }}
        >
          {bottomBarActions}
        </MultiStepFormBottomBar>
      </div>
    );
  }
}

MultiStepForm.propTypes = {
  slides: SlideListPropType.isRequired,
  children: PropTypes.arrayOf(PropTypes.node).isRequired,
  bottomBarActions: PropTypes.node,
  panelClass: PropTypes.string,
};

MultiStepForm.defaultProps = {
  bottomBarActions: undefined,
  panelClass: 'g-mb-0',
};

export default MultiStepForm;
