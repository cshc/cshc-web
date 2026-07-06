import React from 'react';
import PropTypes from 'prop-types';
import GoogleMap from 'components/common/GoogleMap';
import { ViewType } from 'util/constants';
import { ViewSwitcher, ViewSwitcherView } from 'components/common/ViewSwitcher';
import MemberTable from './MemberTable';
import MemberMarker from './MemberMarker';

const MemberListWrapper = ({ 
  canViewMap, 
  data, 
  viewType, 
  onSelectViewType, 
  networkStatus, 
  loading,
  sorted,
  onChangePage,
  onChangeSorted,
  onChangeUrlQueryParams,
  ...props 
}) => {
  const isLoading = loading || networkStatus === 1 || networkStatus === 2 || networkStatus === 4;
  const hasData = data && data.results;
  
  return (
    <div>
      {canViewMap ? (
        <ViewSwitcher currentView={viewType} onSelectViewType={onSelectViewType}>
          <ViewSwitcherView iconClass="fas fa-table" label={ViewType.List} />
          <ViewSwitcherView iconClass="far fa-map" label={ViewType.Map} />
        </ViewSwitcher>
      ) : null}
      {isLoading && (
        <div className="text-center g-py-50">
          <i className="fas fa-spinner fa-spin fa-3x g-color-primary"></i>
          <p className="g-mt-20">Loading members ...</p>
        </div>
      )}
      {!isLoading && hasData && (!canViewMap || viewType === ViewType.List) ? (
        <MemberTable 
          members={data.results} 
          sorted={sorted}
          onChangePage={onChangePage}
          onChangeSorted={onChangeSorted}
          onChangeUrlQueryParams={onChangeUrlQueryParams}
          {...props} 
        />
      ) : !isLoading && hasData && (
        <GoogleMap
          markers={data.results
            .filter(member => member.addrPosition)
            .map(member => <MemberMarker key={member.id} member={member} />)}
        />
      )}
    </div>
  );
};

MemberListWrapper.propTypes = {
  canViewMap: PropTypes.bool.isRequired,
  data: PropTypes.shape(),
  viewType: PropTypes.string.isRequired,
  onSelectViewType: PropTypes.func.isRequired,
  networkStatus: PropTypes.number,
  loading: PropTypes.bool,
  sorted: PropTypes.arrayOf(PropTypes.shape()),
  onChangePage: PropTypes.func.isRequired,
  onChangeSorted: PropTypes.func.isRequired,
  onChangeUrlQueryParams: PropTypes.func.isRequired,
};

MemberListWrapper.defaultProps = {
  data: undefined,
  networkStatus: 7,
  loading: false,
  sorted: [],
};

export default MemberListWrapper;
