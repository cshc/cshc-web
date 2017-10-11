import React from 'react';

type Props = {
  message: ?String,
};

const Loading = ({ message }: Props) => (
  <div>
    <i className="fa fa-lg fa-spinner fa-spin" />
    {message}
  </div>
);

module.exports = Loading;
