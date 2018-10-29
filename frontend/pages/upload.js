import axios from 'axios'
import React, { useState } from 'react'

export default function TimeReportUpload() {
  const [file, setFile] = useState(null)
  const [error, setError] = useState(null)
  const [successMessage, setSuccessMessage] = useState(null)

  return (
    <div>
      <h1>Upload your report CSV here</h1>
      <input accept="text/csv" onChange={onUpload} type="file" />
      <button
        disabled={!file || error}
        onClick={onClickUploadButton}
        submittype="button"
      >
        Upload file
      </button>
      <div>{error}</div>
      <div>{successMessage}</div>
    </div>
  )

  function onUpload(event) {
    if (!event.target.files) {
      return
    }
    setFile(event.target.files[0])
    setError(null)
  }

  function onClickUploadButton() {
    const formData = new FormData()
    formData.append('file', file)
    axios
      .post('http://127.0.0.1:8000/reports/upload', formData)
      .then(({ data }) => {
        const createdTimeReportId = data.time_report_id
        const reportUrl = `/report/${createdTimeReportId}`
        setSuccessMessage(
          <>
            Success! View your uploaded report <a href={reportUrl}>here</a>
          </>,
        )
      })
      .catch(({ response: { data, status } }) => {
        if (status === 409) {
          setError(`Error: ${data}`)
          setFile(null)
        }
      })
  }
}
