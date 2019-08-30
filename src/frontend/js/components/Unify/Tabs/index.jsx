import React from 'react';
import PropTypes from 'prop-types';
import TabNavigation from './TabNavigation';
import TabBlock from './TabBlock';

class Tabs extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      activeTabId: props.items[0].tabId,
    };
    this.selectTab = this.selectTab.bind(this);
  }

  selectTab(tabId) {
    this.setState({ activeTabId: tabId });
  }

  render() {
    const { tabsId, items, unmountInactive } = this.props;
    const { activeTabId } = this.state;
    return (
      <div>
        <ul
          className="nav u-nav-cshc u-nav-primary"
          role="tablist"
          data-target={tabsId}
          data-btn-classes="btn btn-md btn-block u-btn-outline-primary"
        >
          {items.map(item => (
            <TabNavigation
              key={item.tabId}
              title={item.title}
              targetId={item.tabId}
              active={item.tabId === activeTabId}
              onClick={() => this.selectTab(item.tabId)}
            />
          ))}
        </ul>
        <div id={tabsId} className="tab-content g-pt-20">
          {items.map(item => (
            <TabBlock key={item.tabId} id={item.tabId} active={item.tabId === activeTabId}>
              { item.tabId === activeTabId || !unmountInactive ? item.content : null }
            </TabBlock>
          ))}
        </div>
      </div>
    );
  }
}

Tabs.propTypes = {
  items: PropTypes.arrayOf(
    PropTypes.shape({
      tabId: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      content: PropTypes.node.isRequired,
    }),
  ).isRequired,
  tabsId: PropTypes.string,
  unmountInactive: PropTypes.bool,
};

Tabs.defaultProps = {
  tabsId: 'tabs',
  unmountInactive: false,
};

export default Tabs;
