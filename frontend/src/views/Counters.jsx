import React, { useRef, useEffect, useState } from 'react'
import Cookies from 'js-cookie';
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { getMe, userQuerySettings } from '@/queries/auth'
import { getCounterSummary, counterSummaryQuerySettings } from '@/queries/counters'
import TimeSince from '@/components/TimeSince'

const LastLozenge = (props) => {
  const { lastLozenge } = props
  const ref = useRef(null);
  const [compareDate, setCompareDate] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCompareDate(new Date());
    }, 1000);
    return () => clearInterval(interval);
  }, [lastLozenge]);

  return (
    <div className="text-gray-400">
      <p className="text-lg">Last lozenge was <TimeSince from={lastLozenge.date} to={compareDate} /> ago</p>
    </div>
  )
}

const CountButton = (props) => {
  const { name, slug, mutation } = props;
  let displayText = name;

  if (mutation.isLoading) {
    displayText = "Adding {name}..."
  }

  return (
    <button
      className="mt-4 bg-gray-500 hover:bg-gray-700 text-gray-200 font-bold py-4 px-6 border-solid border-2 border-slate-800 rounded"
      onClick={() => mutation.mutate({ count: 1, type_slug: slug })}
    >
      {name}
    </button>
  )
};

const Counters = (props) => {
  const user = useQuery('me', getMe, userQuerySettings)
  const lozenges = useQuery('lozenge-summary', () => getCounterSummary('lozenge'), counterSummaryQuerySettings)
  const queryClient = useQueryClient()

  const addLozenge = useMutation((data) => {
    return fetch('/api/counters/', {
      method: 'POST',
      credentials: 'same-origin',
      headers: {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'X-CSRFToken': Cookies.get('csrftoken'),
      },
      body: JSON.stringify(data)
    })
  }, {
    onSuccess: () => {
      queryClient.invalidateQueries('lozenge-summary')
    }
  }
  );

  if (user.isLoading || lozenges.isLoading) {
    return <div>Loading...</div>
  }

  // Redirect to Django admin if we aren't logged in
  if (user.isError) {
    window.location.href = '/admin/';
  }

  return (
    <div className="m-6 bg-gray-700">
      <h1 className="text-gray-300 text-4xl mb-4">Counters</h1>
      <LastLozenge lastLozenge={lozenges.data.latest_counter} />
      <CountButton name="Lozenge" slug="lozenge" mutation={addLozenge} />
    </div>
  )
}

export default Counters