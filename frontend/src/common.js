export const errorHandler = (err, url) => {
  // if an error occured, we show the appropriate error in English
  // actionStart means all user actions are done, so we can enable the inputs again
  let new_state = {interMsg: "", actionStart: false}

  // most likely backend resource does not exist
  if (err.response?.status === 404) {
    console.error(err.response.data)
    new_state = {...new_state, errorMsg: `Could not find URL: ${url}`}
  }
  // backend error
  if (err.response?.data) {
    console.log(`err occured: ${err.response.data.message}`)
    new_state = {...new_state, errorMsg: err.response.data.message}
  } else {
    // usually a network error
    console.log(`other type of err ${err}`)
    new_state = {...new_state, errorMsg: `${err}`}
  }
  // this will update the state in the parent component
  return new_state
}

export const renderAlert = (state) => {
  // given the state, which has success/error msg, and info about whether or not
  // an action has just been performed, show the appropriate alert
  // if success, show green, if error, show red, if action performed, show spinning wheel
  // as this means we are currently processing request
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
  if (state.actionStart) {
    result.push((
        <div className="d-flex justify-content-center"
             style={{"marginBottom": "2%"}}>
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

// css if we want to center a div horizontally and vertically inside container
export const outerDivStyle = () => {
  return {
    "height": "100vh", "display": "flex", "alignItems": "center",
    "justifyContent": "center"
  }
}
