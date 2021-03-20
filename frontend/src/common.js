export const errorHandler = (err, url) => {
  let new_state = {interMsg: "", actionStart: false}
  if (err.response?.status === 404) {
    console.error(err.response.data)
    new_state = {...new_state, errorMsg: `Could not find URL: ${url}`}
  }
  if (err.response?.data) {
    console.log(`err occured: ${err.response.data.message}`)
    new_state = {...new_state, errorMsg: err.response.data.message}
  } else {
    console.log(`other type of err ${err}`)
    new_state = {...new_state, errorMsg: `${err}`}
  }
  return new_state
}

export const renderAlert = (state) => {
  const result = [];
  if (state.successMsg) {
    result.push((
        <div className="alert alert-success" role="alert">
          {state.successMsg}
        </div>
    ))
  }
  if (state.errorMsg) {
    result.push((
        <div className="alert alert-danger" role="alert">
          {state.errorMsg}
        </div>
    ))
  }
  if (state.interMsg) {
    result.push((
        <div className="d-flex justify-content-center">
          <div className="spinner-border" role="status">
            <span className="sr-only"></span>
          </div>
        </div>
    ))
  }
  return (
      <div>{result}</div>
  )
}
