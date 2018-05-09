import { ApolloClient } from 'apollo-client';
import { createHttpLink } from 'apollo-link-http';
import { ReduxCache } from 'apollo-cache-redux';
import { setContext } from 'apollo-link-context';
import { getCookie } from 'util/cookies';

const csrftoken = getCookie('csrftoken');

const httpLink = createHttpLink({
  uri: '/graphql',
  credentials: 'same-origin',
});

const middlewareLink = setContext(() => ({
  headers: {
    'X-CSRFToken': csrftoken,
  },
}));

const getClient = store =>
  new ApolloClient({
    link: middlewareLink.concat(httpLink),
    cache: new ReduxCache({
      store,
      dataIdFromObject: object => (object.id ? `${object.__typename}-${object.id}` : null),
    }),
  });

module.exports = getClient;
