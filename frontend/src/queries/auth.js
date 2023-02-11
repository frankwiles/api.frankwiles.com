import Cookies from 'js-cookie';

export const userQuerySettings = {
  cacheTime: 60000,
  staleTime: 60000,
  retry: false,
};

export const getMe = async () => {
  const response = await fetch("/api/users/me/", {
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