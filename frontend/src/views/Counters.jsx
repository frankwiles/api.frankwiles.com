import React, { useEffect, useState } from 'react'
import Cookies from 'js-cookie'
import dayjs from 'dayjs'
import { useQuery, useMutation, useQueryClient } from 'react-query'
import { getMe, userQuerySettings } from '@/queries/auth'
import { getCounterSummary, counterSummaryQuerySettings } from '@/queries/counters'
import { HeaderContainer, Header, Breadcrumbs } from '@/components/PageHeader'
import TimeSince from '@/components/TimeSince'

const LastLozenge = (props) => {
  const { lastLozenge } = props
  const [compareDate, setCompareDate] = useState(new Date());

  useEffect(() => {
    const interval = setInterval(() => {
      setCompareDate(new Date())
    }, 1000);
    return () => clearInterval(interval)
  }, [lastLozenge]);

  return (
    <div className="text-gray-400">
      <p className="text-lg">Last lozenge was <TimeSince from={lastLozenge.date} to={compareDate} /> ago</p>
    </div>
  )
}

const CountButton = (props) => {
  const { name, slug, mutation } = props
  let displayText = name

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
}

const LozengeSummary = (props) => {
  const { summary } = props
  let last = dayjs(summary.latest_counter.date)

  return (
    <div className="my-6 text-slate-400">
      <p>Last Lozenge was at {last.format('ddd, MMM D, YYYY h:mm A')}</p>
      <table className="my-6 table-auto">
        <tbody>
          <tr>
            <th className="text-left">Today</th>
            <td className="pl-12 text-right">{summary.today_count}</td>
          </tr>
          <tr>
            <th className="text-left">Last 7 Days Average</th>
            <td className="pl-12 text-right">{summary.last_7_day_average}</td>
          </tr>
          <tr>
            <th className="text-left">Last 30 Days Average</th>
            <td className="pl-12 text-right">{summary.last_30_day_average}</td>
          </tr>
        </tbody>
      </table>
    </div>
  )
}

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
    <div className="m-6">
      <div className="mb-6">
        <Breadcrumbs items={[
          { linkText: 'Home', url: '/homepage/' },
        ]} />
        <HeaderContainer>
          <Header title="Counters" />
        </HeaderContainer>
      </div>
      <LastLozenge lastLozenge={lozenges.data.latest_counter} />
      <CountButton name="Lozenge" slug="lozenge" mutation={addLozenge} />
      <LozengeSummary summary={lozenges.data} />
    </div>
  )
}

export default Counters