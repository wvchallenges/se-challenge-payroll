import React, {Component} from 'react';
import TableRow from "../TableRow/TableRow";
import {v4 as uuidv4} from 'uuid'

class Table extends Component {
  // create the table headers, and for each row passed in, render it as
  // another component
  render() {
    return (
        <div>
          <br/>
          <table className="table table-striped table-bordered">
            <thead className="thead-dark" style={{"textAlign": "center"}}>
            <tr>
              <th scope="col">Employee</th>
              <th scope="col">Pay Start</th>
              <th scope="col">Pay End</th>
              <th scope="col">Pay Amount</th>
            </tr>
            </thead>

            <tbody style={{"textAlign": "center"}}>
            {
              this.props.report["payrollReport"]["employeeReports"].map(row => {
                return <TableRow row={row} key={uuidv4()}/>
              })
            }
            </tbody>
          </table>
        </div>
    );
  }
}

export default Table;
