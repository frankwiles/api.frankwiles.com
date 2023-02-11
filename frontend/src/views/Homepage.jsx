import React from 'react'
import { useQuery } from 'react-query'
import { getMe, userQuerySettings } from '@/queries/auth'

function Homepage() {
  const user = useQuery('me', getMe, userQuerySettings);

  if (user.isLoading) {
    return <div>Loading...</div>
  }

  // Redirect to Django admin if we aren't logged in
  if (user.isError) {
    window.location.href = '/admin/';
  };

  return (
    <div className="m-6">
      <h1 className="text-gray-300 text-4xl">homepage</h1>
      <p>blahblah blah</p>
    </div>
  )
}

export default Homepage