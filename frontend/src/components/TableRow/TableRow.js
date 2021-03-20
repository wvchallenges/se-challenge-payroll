import React, {Component} from 'react';
import {v4 as uuidv4} from 'uuid'

class TableRow extends Component {
  // render our table of report rows
  render() {
    return (
        <tr key={uuidv4()}>
          <th scope="row" key={uuidv4()}>{this.props.row["employeeId"]}</th>
          <td key={uuidv4()}>{this.props.row["payPeriod"]["startDate"]}</td>
          <td key={uuidv4()}>{this.props.row["payPeriod"]["endDate"]}</td>
          <td key={uuidv4()}>{this.props.row["amountPaid"]}</td>
        </tr>
    );
  }
}

export default TableRow;
