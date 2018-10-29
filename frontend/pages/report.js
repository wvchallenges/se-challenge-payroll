import axios from 'axios'
import moment from 'moment'
import PropTypes from 'prop-types'
import { setStatic } from 'recompose'
import React, { useEffect, useState } from 'react'

function TimeReport({ id }) {
  const [reportDetails, setReportDetails] = useState([])
  useEffect(() => {
    axios.get(`http://127.0.0.1:8000/reports/${id}`).then(response => {
      setReportDetails(
        JSON.parse(response.data).map(row => ({
          amountPaid: row.amount_paid,
          employeeId: row.employee_id,
          payPeriodEnd: row.pay_period_end,
          payPeriodStart: row.pay_period_start,
        })),
      )
    })
  }, [])

  return (
    <div>
      <h1>Report {id}</h1>
      {reportDetails.length > 0 && (
        <table border="1">
          {getTableHead()}
          {getTableBody()}
        </table>
      )}
    </div>
  )

  function getTableHead() {
    return (
      <thead>
        <tr>
          <th>Employee ID</th>
          <th>Pay Period</th>
          <th>Amount Paid</th>
        </tr>
      </thead>
    )
  }

  function getTableBody() {
    return <tbody>{reportDetails.map(getReportRow)}</tbody>
  }

  function getReportRow({
    amountPaid,
    employeeId,
    payPeriodStart,
    payPeriodEnd,
  }) {
    const cellKey = `${employeeId} ${payPeriodStart}`
    return (
      <tr key={cellKey}>
        <td key={`${cellKey} id`}>{employeeId}</td>
        <td key={`${cellKey} pay period`}>{`${formatDate(
          payPeriodStart,
        )} - ${formatDate(payPeriodEnd)}`}</td>
        <td key={`${cellKey} amount paid`}>{`$${amountPaid.toFixed(2)}`}</td>
      </tr>
    )
  }

  function formatDate(date) {
    return moment(date).format('D/M/YYYY')
  }
}

TimeReport.propTypes = {
  id: PropTypes.string.isRequired,
  reportDetails: PropTypes.arrayOf(
    PropTypes.shape({
      amountPaid: PropTypes.number,
      employeeId: PropTypes.number,
      payPeriodStart: PropTypes.string,
      payPeriodEnd: PropTypes.string,
    }),
  ).isRequired,
}

const withReportIdFromUrl = setStatic(
  'getInitialProps',
  ({ query: { id } }) => ({ id }),
)
export default withReportIdFromUrl(TimeReport)
