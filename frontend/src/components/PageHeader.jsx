import React from 'react'
import { Link } from "react-router-dom"
import { useNavigate } from "react-router-dom"
import { ChevronLeftIcon, ChevronRightIcon } from '@heroicons/react/20/solid'

export const Header = (props) => {
  const { title } = props
  return (
    <div className="min-w-0 flex-1">
      <h2 className="text-2xl font-bold leading-7 text-white sm:truncate sm:text-3xl sm:tracking-tight">
        {title}
      </h2>
    </div>
  )
}

export const HeaderContainer = (props) => {
  return (
    <div className="mt-2 md:flex md:items-center md:justify-between">
      {props.children}
    </div>
  )
}

export const Breadcrumbs = (props) => {
  const { items } = props
  const lastItem = items[items.length - 1]

  const firstClasses = "text-sm font-medium text-gray-400 hover:text-gray-200"
  const classes = "ml-4 text-sm font-medium text-gray-400 hover:text-gray-200"

  return (
    <div>
      <nav className="sm:hidden" aria-label="Back">
        <Link to={lastItem.url} className="flex items-center text-sm font-medium text-gray-400 hover:text-gray-200">
          <ChevronLeftIcon className="-ml-1 mr-1 h-5 w-5 flex-shrink-0 text-gray-500" aria-hidden="true" />
          Back
        </Link>
      </nav>
      <nav className="hidden sm:flex" aria-label="Breadcrumb">
        <ol role="list" className="flex items-center space-x-4">
          {items.map((item, index) => (
            <li>
              <div className="flex items-center">
                {index !== 0 && <ChevronRightIcon className="h-5 w-5 flex-shrink-0 text-gray-500" aria-hidden="true" />}
                <Link to={item.url} className={index == 0 ? firstClasses : classes}>
                  {item.linkText}
                </Link>
              </div>
            </li>
          ))}
        </ol>
      </nav>
    </div>
  )
}

export const ButtonGroup = (props) => {
  return (
    <div className="mt-4 flex flex-shrink-0 md:mt-0 md:ml-4">
      {props.children}
    </div>
  )
}

const handleButtonClick = (onClick, to, href, navigate) => {
  if (onClick !== undefined) {
    onClick()
  } else if (to !== undefined) {
    navigate(to)
  } else if (href !== undefined) {
    window.location.href = href
  } else {
    throw new Error("Unable to handleButtonClick no proper arguments")
  }
}

export const Button = (props) => {
  const { title, onClick, to, href } = props
  const navigate = useNavigate()

  return (
    <button
      onClick={() => handleButtonClick(onClick, to, href, navigate)}
      type="button"
      className="inline-flex items-center rounded-md border border-transparent bg-gray-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800"
    >
      {title}
    </button>
  )
}

export const PrimaryButton = (props) => {
  const { title, onClick, to, href } = props
  const navigate = useNavigate()
  return (
    <button
      onClick={() => handleButtonClick(onClick, to, href, navigate)}
      type="button"
      className="ml-3 inline-flex items-center rounded-md border border-transparent bg-indigo-500 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-indigo-600 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-gray-800"
    >
      {title}
    </button>
  )
}