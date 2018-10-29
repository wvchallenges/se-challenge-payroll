import axios from 'axios'
import moment from 'moment'
import React, { useEffect, useState } from 'react'

import useTableSorter from '../effects/useTableSorter'

export default function ReportList() {
  const [reports, setReports] = useState([])
  const { getSortedItems, onHeaderClick } = useTableSorter('id')

  useEffect(() => {
    axios.get('http://127.0.0.1:8000/reports/').then(response => {
      setReports(
        response.data.map(report => ({
          id: `${report.id}`,
          dateCreated: report.date_created,
        })),
      )
    })
  }, [])

  return (
    <div>
      <h1>List of reports</h1>
      <table border="1">
        {getTableHead()}
        {getTableBody()}
      </table>
    </div>
  )

  function getTableHead() {
    return (
      <thead>
        <tr>
          <th onClick={onHeaderClick('id')}>Report ID</th>
          <th onClick={onHeaderClick('dateCreated')}>Report ID</th>
        </tr>
      </thead>
    )
  }

  function getTableBody() {
    return <tbody>{getSortedItems(reports).map(getTableRow)}</tbody>
  }

  function getTableRow({ id, dateCreated }) {
    return (
      <tr key={id}>
        <td key={`${id} link`}>
          <a href={`/report/${id}`}>{`Report ${id}`}</a>
        </td>
        <td key={`${id} dateCreated`}>
          {moment(dateCreated).format('D/M/YYYY h:mma')}
        </td>
      </tr>
    )
  }
}
