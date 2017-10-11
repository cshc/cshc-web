import React from 'react';

type Props = {
  error: any,
};

const ErrorDisplay = ({ error }: Props) => <div>{error.message}</div>;

module.exports = ErrorDisplay;
