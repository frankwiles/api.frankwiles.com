import React from 'react'
import { useQuery } from 'react-query'
import { getMe, userQuerySettings } from '@/queries/auth'
import { Link } from "react-router-dom"
import { HeaderContainer, Header } from '@/components/PageHeader'

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
    <div className="m-6 bg-gray-800">
      <HeaderContainer>
        <Header title="Frank's Homepage" />
      </HeaderContainer>
      <p className="my-6">
        <Link
          to="/homepage/counters/"
          className="text-lg text-gray-400 underline hover:text-gray-200">Counters</Link>
      </p>
    </div>
  )
}

export default Homepage