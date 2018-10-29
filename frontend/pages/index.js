import Link from 'next/link'
import React from 'react'

export default () => (
  <div>
    <h1>Payroll Report App</h1>
    <div>
      <Link href="/reports">
        <a>View Time Reports</a>
      </Link>
    </div>

    <div>
      <Link href="/upload">
        <a>Upload Time Report</a>
      </Link>
    </div>
  </div>
)
