import React from 'react';
import { NetworkStatus } from 'apollo-client';
import ErrorDisplay from 'components/common/ErrorDisplay';
import Loading from 'components/common/Loading';

const ViewType = {
  List: 'list',
  Grid: 'grid',
};

type Props = {
  networkStatus: number,
  error: ?Error,
  matches: Array<Object>,
};

type State = {
  viewType: ViewType.List | ViewType.Grid,
};

export default class MatchList extends React.Component<void, Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      viewType: ViewType.List,
    };
  }

  render() {
    const { networkStatus, error, matches } = this.props;
    if (networkStatus === NetworkStatus.loading) return <Loading />;
    if (error) {
      console.error(error);
      return <ErrorDisplay error={error} />;
    }

    return (
      <div>
        <h3>Matches at this venue</h3>
        {matches.edges.map(m => <div key={m.node.id}>{m.node.id}</div>)}
      </div>
    );
  }
}
