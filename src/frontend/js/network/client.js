import { ApolloClient, createNetworkInterface } from 'react-apollo';
import { getCookie } from 'util/cookies';

const csrftoken = getCookie('csrftoken');

const networkInterface = createNetworkInterface({
  uri: '/graphql',
  opts: {
    credentials: 'same-origin',
  },
});

networkInterface.use([
  {
    applyMiddleware(req, next) {
      if (!req.options.headers) {
        req.options.headers = {}; // Create the header object if needed.
      }
      req.options.headers['X-CSRFToken'] = csrftoken;
      next();
    },
  },
]);

const client = new ApolloClient({
  networkInterface,
});

module.exports = client;
