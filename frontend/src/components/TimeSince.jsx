import React from 'react'
import dayjs from 'dayjs'

const TimeSince = (props) => {
    /*
    Given a datetime, return 00:00:00 of hours, minutes and seconds since
    then
    */
    const { from, to } = props
    const last = dayjs(from)
    let start = null

    if (to === null) {
        start = new Date();
    }
    else {
        start = dayjs(to)
    }

    const total = start - last
    const seconds = Math.floor((total / 1000) % 60)
    const minutes = Math.floor((total / 1000 / 60) % 60)
    const hours = Math.floor((total / 1000 / 60 / 60) % 24)

    const zeroPad = (num) => {
        if (num < 0) {
            return '00'
        }
        return (num > 9 ? num : '0' + num)
    }

    return (
        <span {...props}>{zeroPad(hours)}:{zeroPad(minutes)}:{zeroPad(seconds)}</span>
    )
}

export default TimeSince