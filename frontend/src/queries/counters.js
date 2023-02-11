import Cookies from 'js-cookie';

export const counterSummaryQuerySettings = {
  cacheTime: 10000,
  staleTime: 5000,
};

export const getCounterSummary = async (slug) => {
  const response = await fetch(`/api/counters/summary/${slug}`, {
    method: 'GET',
    credentials: 'same-origin',
    headers: {
      'Accept': 'application/json',
      'Content-Type': 'application/json',
      'X-CSRFToken': Cookies.get('csrftoken'),
    }
  });

  if (!response.ok) {
    throw new Error(response.statusText);
  }

  const data = await response.json();

  return data;
}