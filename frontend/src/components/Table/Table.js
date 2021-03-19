import React, {Component} from 'react';
import { v4 as uuidv4 } from 'uuid'

class Table extends Component {
  render() {
    return (
        <div>
          <br/>
          <table className="table table-striped table-bordered">
            <thead className="thead-dark" style={{"textAlign":"center"}}>
            <tr>
              <th scope="col">Employee</th>
              <th scope="col">Pay Start</th>
              <th scope="col">Pay End</th>
              <th scope="col">Pay Amount</th>
            </tr>
            </thead>

          <tbody style={{"textAlign":"center"}}>
          {
            this.props.report["payrollReport"]["employeeReports"].map(rep => {
              return (
                  <tr key={uuidv4()}>
                    <th scope="row">{rep["employeeId"]}</th>
                    <td>{rep["payPeriod"]["startDate"]}</td>
                    <td>{rep["payPeriod"]["endDate"]}</td>
                    <td>{rep["amountPaid"]}</td>
                  </tr>
              )
            })
          }
          </tbody>
          </table>



          {/*<pre>*/}
          {/*  {JSON.stringify(this.props.report["payrollReport"]["employeeReports"])}*/}
          {/*</pre>*/}
        </div>
    );
  }
}

export default Table;
